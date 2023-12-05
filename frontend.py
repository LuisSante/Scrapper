import requests

def main():
    url = "http://127.0.0.1:8080/execute" 

    try:
        response = requests.post(url)
        response_ = response.json()

        if response.status_code == 200:
            print("Petición POST exitosa")
            print("Respuesta:", response_['result'])
        else:
            print(f"Error en la petición. Código de respuesta: {response.status_code}")
            print("Contenido de la respuesta:", response.text)
    except Exception as e:
        print(f"Error en la petición: {e}")

if __name__ == "__main__":
    main()
