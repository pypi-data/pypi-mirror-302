import logging
import unittest

from src.ai_models.ai_tools import AITools
from src.ai_models.object_detection import ObjectDetectionModel

logger = logging.getLogger("test_object_detection")
logger.setLevel(logging.INFO)


class TestLargeLanguageModel(unittest.TestCase):
    def test_object_detection_model_health(self):
        for model in ObjectDetectionModel:
            self.assertTrue(AITools.object_detection_health(model))
