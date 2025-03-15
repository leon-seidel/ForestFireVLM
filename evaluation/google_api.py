from google import genai
from google.genai import types
from PIL import Image
import time
import os

class GoogleAPI:
    def __init__(self, model_name, temperature=0.0):
        # Setup VLM API
        self.model_name = model_name
        self.temperature = temperature
        api_key = os.environ["GOOGLE_API_KEY"]
        self.client = genai.Client(api_key=api_key)
        print(f"Connected to {self.model_name}")

    def generate_structured_response_from_pil_image(self, full_prompt: str, pil_image: Image.Image, 
                                                    response_schema: type) -> str:
        config = types.GenerateContentConfig(temperature=self.temperature, response_mime_type="application/json",
                                             response_schema=response_schema)

        while True:
            try:
                response = self.client.models.generate_content(model=self.model_name, 
                                        contents=[pil_image, full_prompt], config=config)
                break
            except Exception as e:
                print(f"Error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

        return response.text
