import os
import base64
import requests
from google import genai
from PIL import Image
import config
import abc
import io
from google.genai import types

class VLMEngineBase(abc.ABC):
    @abc.abstractmethod
    def generate_description(self, title, location, image_path, description, tasks, comments="") -> str:
        pass

class GeminiVLMEngine(VLMEngineBase):
    def __init__(self, api_key: str = None, model_name: str = "gemini-2.0-flash"):
        # Usar API Key si se proporciona
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate_description(self, title, location, image_path, description, tasks, comments="") -> str:
        try:
            # Load and process the image
            image = self._load_image(image_path)
            
            # Create prompt
            prompt_user = self._create_prompt(title, location, description, tasks, comments)
            
            # Generate content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt_user, image],
                config=types.GenerateContentConfig(
                    system_instruction="You are an AI assistant that generates narrative descriptions for presentation slides. Only answer with the explanation of the slide, nothing else.",
                    max_output_tokens=500,
                    temperature=0.1
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating description with Gemini: {str(e)}")
            raise

    def _load_image(self, image_obj):
        if isinstance(image_obj, bytes):
            return Image.open(io.BytesIO(image_obj))
        elif hasattr(image_obj, "read"):
            return Image.open(image_obj)
        elif isinstance(image_obj, str):
            return Image.open(image_obj)
        else:
            raise ValueError("Formato de imagen no reconocido")

    def _create_prompt(self, title, location, description, tasks, comments):
        prompt = f"""
        Genera una narración natural en español para una persona invidente que describa la siguiente planta de un huerto urbano:
        
        Nombre de la planta: {title}
        Ubicación: {location}
        Descripción: {description}
        Tareas pendientes: {tasks}
        """
        
        if comments:
            prompt += f"\nComentarios adicionales: {comments}"
            
        prompt += """
        
        Detalles importantes:
        - La narración debe ser descriptiva pero concisa (máximo 150 palabras)
        - Describe visualmente la planta según la imagen proporcionada
        - Usa un tono amigable y cercano
        - Menciona específicamente las tareas que hay que realizar
        - Organiza la información de forma clara y estructurada
        """
        return prompt

def get_vlm_instance() -> VLMEngineBase:
    model_name = config.VLM_MODEL.lower()
    
    if "gemini" in model_name:
        return GeminiVLMEngine(config.VLM_API_KEY, config.VLM_MODEL_NAME)
    else:
        raise ValueError(f"VLM model '{model_name}' not supported")

def generate_description(title, location, image_path, description, tasks, comments=""):
    """
    Generate a textual narration from plant data using a VLM model.
    
    Args:
        title: Title of the plant
        location: Location of the plant in the garden
        image_path: Path to the plant image
        description: Description of the plant
        tasks: Current tasks to be performed on the plant
        comments: Optional comments about the plant
        
    Returns:
        Generated text narration
    """
    vlm_engine = get_vlm_instance()
    return vlm_engine.generate_description(title, location, image_path, description, tasks, comments)