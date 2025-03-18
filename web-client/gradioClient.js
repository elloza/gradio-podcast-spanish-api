// gradioClient.js

export async function generateNarration(apiUrl, inputData) {
    try {
      // Paso 1: Enviar solicitud POST para obtener el event_id
      const postResponse = await fetch(`${apiUrl}/gradio_api/call/process_inputs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: inputData })
      });
  
      if (!postResponse.ok) {
        throw new Error(`Error en la solicitud POST: ${postResponse.status}`);
      }
  
      const postResult = await postResponse.json();
      const eventId = postResult["event_id"];
  
      console.log(`Obtenido event_id: ${eventId}`);
  
      // Paso 2: Realizar solicitud GET para obtener el resultado
      const getResponse = await fetch(`${apiUrl}/gradio_api/call/process_inputs/${eventId}`, {
        method: "GET"
      });
  
      if (!getResponse.ok) {
        throw new Error(`Error en la solicitud GET: ${getResponse.status}`);
      }
  
      const getResult = await getResponse.json();
  
      // Retornar los datos extraídos
      return {
        audioUrl: apiUrl + "/file=" + getResult.data[0], // Ruta del audio generado
        narrationText: getResult.data[1] // Texto generado
      };
  
    } catch (error) {
      console.error("Error al generar la narración:", error);
      throw error;
    }
  }
  