# FAIsdk/FAImageGen/__init__.py
from .api_client import APIClient
from .image_generation import ImageGeneration
from .harmonizer import Harmonizer
from .fuzer import Fuzer

class ImageGen:
    def __init__(self, base_url, api_key, email):
        self.client = APIClient(base_url, api_key, email)
        self.image_generation = ImageGeneration(self.client)
        self.harmonizer = Harmonizer(self.client)
        self.fuzer = Fuzer(self.client)
        

