import os
import tempfile
import requests
from pathlib import Path
import torch
import config
import numpy as np
import io
import soundfile as sf
from TTS.api import TTS
import abc

os.environ["COQUI_TOS_AGREED"] = "1"

class TTSEngine(abc.ABC):
    @abc.abstractmethod
    def get_available_voices(self) -> dict:
        pass

    @abc.abstractmethod
    def get_available_languages(self) -> dict:
        pass

    @abc.abstractmethod
    def synthesize_text(self, voice_id: str, text: str, language:str, **kwargs) -> bytes:
        pass

class XTTSv2(TTSEngine):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(XTTSv2, cls).__new__(cls)
            cls._instance.voices = [
                "Aaron Dreschner", "Abrahan Mack", "Adde Michal", "Alexandra Hisakawa", "Alison Dietlinde",
                "Alma María", "Ana Florence", "Andrew Chipper", "Annmarie Nele", "Asya Anara", "Badr Odhiambo",
                "Baldur Sanjin", "Barbora MacLean", "Brenda Stern", "Camilla Holmström", "Chandra MacFarland",
                "Claribel Dervla", "Craig Gutsy", "Daisy Studious", "Damien Black", "Damjan Chapman",
                "Dionisio Schuyler", "Eugenio Mataracı", "Ferran Simen", "Filip Traverse", "Gilberto Mathias",
                "Gitta Nikolina", "Gracie Wise", "Henriette Usha", "Ige Behringer", "Ilkin Urbano", "Kazuhiko Atallah",
                "Kumar Dahl", "Lidiya Szekeres", "Lilya Stainthorpe", "Ludvig Milivoj", "Luis Moray", "Maja Ruoho",
                "Marcos Rudaski", "Narelle Moon", "Nova Hogarth", "Rosemary Okafor", "Royston Min", "Sofia Hellen",
                "Suad Qasim", "Szofi Granger", "Tammie Ema", "Tammy Grit", "Tanja Adelina", "Torcull Diarmuid",
                "Uta Obando", "Viktor Eka", "Viktor Menelaos", "Vjollca Johnnie", "Wulf Carlevaro", "Xavier Hayasaka",
                "Zacharie Aimilios", "Zofija Kendrick"
            ]
            cls._instance.language_codes = {
                "en": "English", "es": "Spanish", "fr": "French", "de": "German", "it": "Italian",
                "pt": "Portuguese", "pl": "Polish", "tr": "Turkish", "ru": "Russian", "nl": "Dutch",
                "cs": "Czech", "ar": "Arabic", "zh-cn": "Chinese", "ja": "Japanese", "hu": "Hungarian",
                "ko": "Korean", "hi": "Hindi"
            }
            cls._instance.device = "cuda" if torch.cuda.is_available() else "cpu"
            cls._instance.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(cls._instance.device)
        return cls._instance

    def get_available_voices(self) -> dict:
        return {voice: voice for voice in self.voices}
    
    def get_available_languages(self) -> dict:
        return {code: lang for code, lang in self.language_codes.items()}

    def synthesize_text(self, voice_id: str, text: str, language:str, **kwargs) -> bytes:
        try:
            result = self.model.tts(text=text, speaker=voice_id, language=language)
            audio = np.array(result)
            with io.BytesIO() as output:
                sf.write(output, audio, 24000, format='WAV')
                return output.getvalue()
        except Exception as e:
            return b""
        

# TTS factory from config
def get_tts_instance() -> TTSEngine:
    if config.TTS_ENGINE == "xttsv2":
        return XTTSv2()
    else:
        raise ValueError("TTS engine not supported")