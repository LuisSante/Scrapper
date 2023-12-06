import './App.css';
import React, { useState, useEffect } from 'react';

function App() {
  const [respuestaApi, setRespuestaApi] = useState(null);

  useEffect(() => {
    const enviarSolicitud = async () => {
      // const url = "http://127.0.0.1:8080/execute";
      const url = "https://imagespider-2fk5vwiqyq-tl.a.run.app/execute";

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Petición POST exitosa");
          console.log("Respuesta:", data.result);
          setRespuestaApi(data.result);
        } else {
          console.error(`Error en la petición. Código de respuesta: ${response.status}`);
          console.error("Contenido de la respuesta:", await response.text());
        }
      } catch (error) {
        console.error(`Error en la petición: ${error.message}`);
      }
    };

    enviarSolicitud();
  }, [])

  return (
    <div>
      <h1>Consumir API con método POST en React</h1>

      {respuestaApi && (
        <div>
          <h2>Respuesta de la API:</h2>
          <pre>{JSON.stringify(respuestaApi, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
