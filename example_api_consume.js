// Example of consuming the Gradio API via a POST request using fetch
const apiUrl = 'http://localhost:7860/api/predict'; // adjust port if needed

const postData = {
  data: [
    "Tomate Cherry",                // title
    "Parcela 3, Fila 2",              // location
    "/path/to/plant_image.jpg",       // plant_image (file path or URL)
    "Planta con hojas verdes.",       // description
    "Riego, poda",                    // tasks
    "Sin comentarios adicionales"     // comments (optional)
  ]
};

fetch(apiUrl, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(postData)
})
.then(response => response.json())
.then(data => {
  console.log('API response:', data);
})
.catch(error => {
  console.error('Error calling API:', error);
});
