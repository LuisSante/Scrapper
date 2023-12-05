import requests

def main():
    url = "https://temp-spider2-2fk5vwiqyq-uc.a.run.app/execute" 

    try:
        response = requests.post(url)

        if response.status_code == 200:
            print("Petición POST exitosa")
            print("Respuesta:", response.json())
        else:
            print(f"Error en la petición. Código de respuesta: {response.status_code}")
            print("Contenido de la respuesta:", response.text)
    except Exception as e:
        print(f"Error en la petición: {e}")

if __name__ == "__main__":
    main()
