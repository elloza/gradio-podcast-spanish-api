# Gradio Endpoint para generar una narración a partir de datos de entrada

Se trata de una perqueña PoC para generar un audio a partir de datos de entrada.

La idea general es convertir, por ejemplo, toda la información que se tiene sobre una entidad de información de un software, supongamos en una aplicación de gestión de huertos urbanos la información de una planta, en una narración que pueda ser escuchada por una persona invidente.

1. La aplicación recibirá los siguientes datos de entrada:

- Titulo de la planta
- Ubicación de la planta en el huerto
- Imagen de la planta
- Descripción de la planta
- Tareas actuales que hay que realizar en la planta
- Comentarios sobre la planta (opcional)

2. Con esta información, un modelo VLM como Gemini 2.0 Ultra generará un texto que describe la planta y las tareas que hay que realizar en ella junto con los comentarios.

3. Una vez generado el texto, se utilizará un modelo de TTS para generar la narración en audio en español.

4. El audio generado se devolverá y se mostrará como un control de audio en la interfaz web y en el caso de la API ofrecida por Gradio se devolverá un archivo de audio.

## Tecnologías utilizadas

Para ello se utilizan las siguientes tecnologías:

- [Gradio](https://gradio.app/): Se utilizará gradio para generar tanto una API como una interfaz web para poder generar la narración a partir de unos datos de entrada.

- VLM: Se utilizará un modelo de VLM para generar un texto a partir de los datos de entrada. Algunos de los modelos que se podrán utilizar son:
    - [Gemini 2.0 Ultra] [API]
    - [Qwen2.5 VL]

- [TTS model]: Se utilizará un modelo de TTS para generar la narración a partir de los datos de entrada. Algunos de los modelos que se podrán utilizar son:
    - [Kokoro]
    - [Coqui TTS]
    - [Zonos]

Se crearán los siguientes recursos para integrar y desplegar esta API también:

* Un script que permita probarlo desde una web local y que muestre la narración generada en un control de audio en JavaScript

* Un dockerfile para poder desplegarlo en un contenedor en una máquina remota VPS.

## 🚀 ¡Manos a la obra! - Guía de uso

### 📋 Requisitos previos

- Python 3.8+ 🐍
- Pip 📦
- Docker 🐳 (opcional, para despliegue en contenedor)
- Ganas de experimentar! 💪

### 🔧 Instalación 

1. **Clona el repo** ✨
   // ...instrucciones existentes...

2. **Prepara tu entorno mágico** 🧙‍♂️
   // ...instrucciones existentes...

## 🔑 Configuración para Despliegue

### Archivo de configuración (.env)

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido: