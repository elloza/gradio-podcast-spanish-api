import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server configuration
PORT = int(os.getenv("PORT", "7860"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Directory paths
BASE_DIR = Path(__file__).resolve().parent
AUDIO_OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "audio")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

# Create necessary directories if they don't exist
for directory in [AUDIO_OUTPUT_DIR, UPLOADS_DIR]:
    os.makedirs(directory, exist_ok=True)

# VLM Model Configuration
VLM_MODEL = os.getenv("VLM_MODEL", "gemini")

VLM_MODEL_NAME = os.getenv("VLM_MODEL_NAME", "gemini")
VLM_API_KEY = os.getenv("VLM_API_KEY","")
VLM_URL = os.getenv("VLM_URL","https://api.visionlanguage.io/v1/")

# TTS Configuration
TTS_ENGINE = os.getenv("TTS_ENGINE", "xttsv2") 
