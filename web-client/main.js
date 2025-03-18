// main.js
import { generateNarration } from "./gradioClient.js";

const apiUrl = "https://8b63c908225c65191f.gradio.live"; // URL de tu servidor Gradio

document.getElementById("generateBtn").addEventListener("click", async () => {
  const inputData = [
    "Hello!!",
    "Hello!!",
    { path: "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fnatursan.net%2Fwp-content%2Fbeneficios-tomate.jpg" },
    "Hello!!",
    "Hello!!",
    "Hello!!",
    "en",
    "Aaron Dreschner"
  ];

  try {
    const { audioUrl, narrationText } = await generateNarration(apiUrl, inputData);
    document.getElementById("audioPlayer").src = audioUrl;
    document.getElementById("textResult").innerText = narrationText;
  } catch (error) {
    document.getElementById("textResult").innerText = `Error: ${error.message}`;
  }
});
