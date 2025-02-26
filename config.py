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
VLM_MODEL = os.getenv("VLM_MODEL", "gemini")  # Options: "gemini", "qwen"

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-1.5-pro-vision")

# Qwen Configuration (placeholder)
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "Qwen/Qwen2.5-VL")

# TTS Configuration
TTS_MODEL = os.getenv("TTS_MODEL", "coqui")  # Options: "kokoro", "coqui", "zonos"

# Kokoro TTS Configuration
KOKORO_API_KEY = os.getenv("KOKORO_API_KEY", "")

# Zonos TTS Configuration
ZONOS_API_KEY = os.getenv("ZONOS_API_KEY", "")
