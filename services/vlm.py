import os
import base64
import requests
import google.generativeai as genai
from PIL import Image
import config

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
    # Select which VLM model to use based on configuration
    model_name = config.VLM_MODEL.lower()
    
    if "gemini" in model_name:
        return _generate_with_gemini(title, location, image_path, description, tasks, comments)
    elif "qwen" in model_name:
        return _generate_with_qwen(title, location, image_path, description, tasks, comments)
    else:
        raise ValueError(f"VLM model '{model_name}' not supported")

def _generate_with_gemini(title, location, image_path, description, tasks, comments=""):
    """
    Generate narration using Google's Gemini model.
    """
    try:
        # Configure the Gemini API
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)
        
        # Load and process the image
        image = Image.open(image_path)
        
        # Create prompt
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
        
        # Generate content
        response = model.generate_content([prompt, image])
        
        return response.text
        
    except Exception as e:
        print(f"Error generating description with Gemini: {str(e)}")
        raise

def _generate_with_qwen(title, location, image_path, description, tasks, comments=""):
    """
    Generate narration using Qwen VL model.
    """
    try:
        # This is a placeholder for Qwen integration
        # In a real implementation, you would use the appropriate API or model
        
        # Read image as base64
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Create prompt
        prompt = f"""
        Genera una narración natural en español para una persona invidente que describa la siguiente planta de un huerto urbano:
        
        Nombre de la planta: {title}
        Ubicación: {location}
        Descripción: {description}
        Tareas pendientes: {tasks}
        """
        
        if comments:
            prompt += f"\nComentarios adicionales: {comments}"
        
        # Example API call to Qwen model (placeholder)
        # In a real scenario, this would be implemented with the actual Qwen API
        
        # Placeholder response
        narration = f"""
        Esta es la planta {title} ubicada en {location}. {description}. 
        Actualmente, se necesita {tasks}.
        """
        
        if comments:
            narration += f" Nota: {comments}."
            
        return narration
        
    except Exception as e:
        print(f"Error generating description with Qwen: {str(e)}")
        raise
