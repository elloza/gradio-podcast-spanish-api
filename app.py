import os
import tempfile
import gradio as gr

import config
from services.tts import get_tts_instance
from services.vlm import get_vlm_instance

tts_instance = get_tts_instance()
vlm_instance = get_vlm_instance()
available_voices = tts_instance.get_available_voices()
available_languages = tts_instance.get_available_languages()

def process_inputs(
    title, 
    location, 
    plant_image, 
    description, 
    tasks,
    comments="",
    language="es",
    voice="Aaron Dreschner"
):
    """
    Process the input data and generate an audio narration.
    
    Args:
        title: Title of the plant
        location: Location of the plant in the garden
        plant_image: Image of the plant
        description: Description of the plant
        tasks: Current tasks to be performed on the plant
        comments: Optional comments about the plant
        language: Language for the narration
        voice: Voice for the narration
        
    Returns:
        Audio file path with the generated narration
    """
    try:
        # Step 1: Generate a textual description using VLM
        narration_text = vlm_instance.generate_description(
            title=title,
            location=location,
            image_path=plant_image,
            description=description,
            tasks=tasks,
            comments=comments
        )
        
        # Step 2: Generate audio from the text
        audio_path = tts_instance.synthesize_text(voice, narration_text, language)
        
        return audio_path, narration_text
    
    except Exception as e:
        error_message = f"Error generando la narración: {str(e)}"
        print(error_message)
        return None, error_message

# Create Gradio interface with two main columns: left (inputs) and right (results)
with gr.Blocks(title="Narración de Plantas para Invidentes") as demo:
    gr.Markdown("# 🌱 Narrador de Plantas para Huertos Urbanos")
    gr.Markdown("""
    Esta aplicación convierte la información de una planta en una narración de audio para personas con discapacidad visual.
    Proporcione los datos de la planta y genere una descripción narrada.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Datos de Entrada")
            title_input = gr.Textbox(label="Título de la Planta", placeholder="Ej: Tomate Cherry")
            location_input = gr.Textbox(label="Ubicación en el Huerto", placeholder="Ej: Parcela 3, Fila 2")
            plant_image_input = gr.Image(type="filepath", label="Imagen de la Planta")
            description_input = gr.Textbox(
                label="Descripción de la Planta", 
                placeholder="Describa las características principales de la planta...",
                lines=3
            )
            tasks_input = gr.Textbox(
                label="Tareas Pendientes", 
                placeholder="Enumere las tareas que hay que realizar con la planta...",
                lines=3
            )
            comments_input = gr.Textbox(
                label="Comentarios (opcional)", 
                placeholder="Comentarios adicionales sobre la planta...",
                lines=2
            )
            language_input = gr.Dropdown(label="Idioma", choices=list(available_languages.keys()), value="es")
            voice_input = gr.Dropdown(label="Voz", choices=list(available_voices.keys()), value="Aaron Dreschner")
            gr.Markdown("#### Ejemplos de muestra")
            gr.Examples(
                examples=[
                    ["Tomate Cherry", "Parcela 3, Fila 2", "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2F2.bp.blogspot.com%2F-Vmyqu3sctRg%2FVb3lOq3IHtI%2FAAAAAAAAhhQ%2FUWCU8xDFT2o%2Fs1600%2Faa1.jpg&f=1&nofb=1&ipt=809814dd2e1c3254276f330d056988bf0c99f843e8235a4d4612366f729f901d&ipo=images", "Planta de tomate con frutos pequeños", "Riego diario", ""],
                    ["Lechuga", "Invernadero", "https://www.jardineriaon.com/wp-content/uploads/2019/10/Lechuga-batavia.jpg", "Planta de lechuga fresca", "Fertilización semanal", ""]
                ],
                inputs=[title_input, location_input, plant_image_input, description_input, tasks_input, comments_input],
                cache_examples=False
            )
            generate_btn = gr.Button("Generar Narración", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("### Resultados")
            audio_output = gr.Audio(label="Audio Generado", interactive=False)
            text_output = gr.Textbox(label="Texto Generado", lines=5)

    generate_btn.click(
        fn=process_inputs, 
        inputs=[
            title_input, 
            location_input, 
            plant_image_input, 
            description_input, 
            tasks_input,
            comments_input,
            language_input,
            voice_input
        ],
        outputs=[audio_output, text_output]
    )

# API endpoints
demo.queue().launch(server_name="0.0.0.0", server_port=config.PORT,share=True)
