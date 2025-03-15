from openai import OpenAI
import time
from PIL import Image
import base64
from io import BytesIO
import os

class OpenAIAPI:
    def __init__(self, base_url="http://localhost:8000/v1", model_name=None, temperature=0.0):
        # Setup VLM API
        self.model_name = model_name 
        self.temperature = temperature
        self.connection_timeout = 5  # Time to wait before trying to connect again
        self.vlm_client = self.connect_to_vlm(base_url)

        if model_name is None:
            self.model_name = self.vlm_client.models.list().data[0].id
        else:
            self.model_name = model_name
        print(f"Connected to {self.model_name}")

    def connect_to_vlm(self, base_url):
        while True:
            try:
                if base_url == None:
                    api_key = os.environ["OPENAI_API_KEY"]
                else:
                    api_key = "empty"
                print("Connecting to OpenAI API endpoint...")
                vlm_client = OpenAI(api_key=api_key, base_url=base_url)
                return vlm_client
            except Exception as e:
                print("No model on this API yet...", e)
                time.sleep(self.connection_timeout)
                continue   
    
    def generate_structured_response_from_pil_image(self, full_prompt: str, pil_image: Image.Image, 
                                                    response_schema: dict) -> str:
        chat_completion_from_base64 = self.vlm_client.chat.completions.create(
            messages=self.create_vlm_messages(full_prompt, pil_image),
            model=self.model_name,
            temperature=self.temperature,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "strict": True,
                    "schema": response_schema,
                },
            }
        )
        return chat_completion_from_base64.choices[0].message.content

    def create_vlm_messages(self, full_prompt: str, pil_image: Image.Image) -> list[dict]:
        image_url = f"data:image/jpeg;base64,{self.pil_image_to_base64(pil_image)}"
        messages=[
                    {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": full_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                                },
                        },
                        ]
                    }
                ]
        return messages
    

    def pil_image_to_base64(self, pil_image: Image.Image) -> str:
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    