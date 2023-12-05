import scrapy
from scrapy_user_agents.middlewares import RandomUserAgentMiddleware
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from scrapy.spidermiddlewares.offsite import OffsiteMiddleware
import os

class VerifyLinksSpider(scrapy.Spider):
    name = 'verify_links'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'RETRY_TIMES': 5,   # Número máximo de reintentos permitidos
        'RETRY_DELAY': 10,  # Tiempo de espera (en segundos) entre reintentos
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
        # Manejar errores aquí (por ejemplo, códigos de estado 503)
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
