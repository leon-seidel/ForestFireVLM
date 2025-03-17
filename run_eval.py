import argparse
from datasets import load_dataset
from evaluation.forestfire_evaluation import create_predictions, eval_structured_data


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
    parser.add_argument('--dataset_name', type=str, help='Dataset name', default="leon-se/ForestFireInsights-Eval")
    parser.add_argument('--ds_split', type=str, help='Dataset split', default="train")
    parser.add_argument('--results_folder', type=str, help='Folder to save results', default="benchmarks")

    # Parse args
    args = parser.parse_args()

    # Setup
    vlm = setup_vlm(args)
    eval_ds = load_dataset(args.dataset_name, split=args.ds_split)

    # Create predictions
    predictions_text, ground_truth_dicts = create_predictions(eval_ds, vlm)

    # Evaluate predictions
    eval_structured_data(predictions_text, ground_truth_dicts, vlm.model_name, args.dataset_name, write_to_file=True, 
                         results_folder=args.results_folder)


if __name__ == "__main__":
    main()
