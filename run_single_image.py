import argparse
from PIL import Image
import requests
from io import BytesIO
from templates.answer_schema import smoke_detection_schema
from templates.prompt import smoke_detection_prompt 

def setup_vlm(args):
    if args.backend == "google":
        from evaluation.google_api import GoogleAPI
        vlm = GoogleAPI(model_name=args.model_name)
    elif args.backend == "openai":
        from evaluation.openai_api import OpenAIAPI
        vlm = OpenAIAPI(base_url=None, model_name=args.model_name)
    elif args.backend == "vllm_online":
        from evaluation.openai_api import OpenAIAPI
        vlm = OpenAIAPI(base_url=args.vllm_url, model_name=None)
    else:
        raise ValueError("Invalid backend")
    return vlm


def main():
    # Create CLI args
    parser = argparse.ArgumentParser(description='Evaluate a VLM model on a structured dataset')
    parser.add_argument('--backend', type=str, help='VLM backend', default="vllm_online")
    parser.add_argument('--vllm_url', type=str, help='URL for vLLM', default="http://localhost:8000/v1")
    parser.add_argument('--model_name', type=str, help='VLM model name', default="")
    parser.add_argument('--image', type=str, help='Local path to image or image URL')

    # Parse args
    args = parser.parse_args()

    # Setup
    vlm = setup_vlm(args)

    # Load image
    if args.image.startswith("http"):
        response = requests.get(args.image)
        pil_image = Image.open(BytesIO(response.content))
    else:
        pil_image = Image.open(args.image)

    # Create prediction
    vlm_prediction = vlm.generate_structured_response_from_pil_image(smoke_detection_prompt, pil_image, smoke_detection_schema)
    print(vlm_prediction)

if __name__ == "__main__":
    main()
