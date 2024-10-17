from .client import DangquSdk
from .OCR import OCR, OCRConfig
from .slider import get_slide_track, generate_trajectory, SliderTrajectory

__all__ = ['DangquSdk', "OCR", 'OCRConfig', 'SliderTrajectory', 'generate_trajectory', 'get_slide_track']
