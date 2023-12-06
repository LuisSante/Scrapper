import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

class VerifyLinksSpider(scrapy.Spider):
    name = 'verify_links'

    custom_settings = {
        'USER_AGENTS': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/14.1.2',
            'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Android 11; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0',
            'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.62 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/14.1.2',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 11; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        ],
        'RETRY_TIMES': 40, 
        'RETRY_DELAY': 5,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        },
    }

    allowed_domains = [
        "amazon.com"
    ]

    def __init__(self, *args, **kwargs):
        super(VerifyLinksSpider, self).__init__(*args, **kwargs)
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        links_file_path = os.path.join(current_dir, 'links.txt')

        with open(links_file_path, 'r') as file:
            urls = file.readlines()

        self.start_urls = [url.strip() for url in urls]

    def parse(self, response):
        for title in response.css('div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small'):
            yield {
                "product": title.css('span.a-size-base-plus.a-color-base.a-text-normal::text').get(),
                "record": title.css('span.a-icon-alt::text').get(),
                "reviews": title.css('span.a-size-base.s-underline-text::text').get(),
                "sales": title.css('span.a-size-base.a-color-secondary::text').get(),
                "price": title.css('span.a-offscreen::text').get(),
            }

        next_page = response.css('a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator::attr("href")').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, errback=self.error_handler)

    def error_handler(self, failure):
        request = failure.request
        self.logger.error(f"Error on {request.url}: {repr(failure)}")
        
        retries = request.meta.get('retry_times', 0) + 1
        retry_times = self.crawler.settings.getint('RETRY_TIMES')
        if retries <= retry_times:
            retry_request = request.copy()
            retry_request.meta['retry_times'] = retries
            retry_request.dont_filter = True
            retry_request.priority = request.priority + self.crawler.settings.getint('RETRY_PRIORITY_ADJUST')
            return retry_request
        else:
            self.logger.warning(f"Giving up retrying {request.url} (failed {retries} times)")
            return None