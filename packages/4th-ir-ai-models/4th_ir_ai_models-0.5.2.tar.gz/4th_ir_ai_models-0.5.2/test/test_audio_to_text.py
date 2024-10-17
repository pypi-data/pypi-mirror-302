import logging
import unittest

from src.ai_models.ai_tools import AITools
from src.ai_models.audio_to_text import AudioToTextModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestImageClassification(unittest.TestCase):
    def test_speech_to_text_health(self):
        for model in AudioToTextModel:
            self.assertTrue(AITools.speech_to_text_health(model))
