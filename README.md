# ForestFireVLM

ForestFireVLM is a framework for evaluating Vision Language Models (VLMs) on forest fire detection and analysis tasks. The framework provides structured evaluation methods to assess how well different VLMs can identify smoke, flames, fire characteristics, and potential hazards from aerial imagery.

## About the paper

*This section will be updated when the paper is published.*

This code accompanies a research paper currently under peer review with MDPI. The paper explores the application of Vision Language Models for automated forest fire detection and analysis from aerial imagery.

**Links:**
- Paper: [Link to be added upon publication]
- Models and Dataset Collection: [HuggingFace](https://huggingface.co/collections/leon-se/forestfirevlm-67d3429a77d9a5fc6c7ce9f5)
- Models: [Link to be added upon publication]

## Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ForestFireVLM.git
cd ForestFireVLM

# Install dependencies
pip install -r requirements.txt

# Set up API keys (if needed)
export OPENAI_API_KEY="your_openai_api_key_here"
export GOOGLE_API_KEY="your_google_api_key_here"
```

## Usage

### Evaluating Models

The main evaluation script `run_eval.py` supports multiple VLM backends and evaluation options:

#### Using OpenAI Models

```bash
python evaluation/run_eval.py \
  --backend openai \
  --model_name gpt-4o \
  --dataset_name leon-se/forestfire_vlm_v6_eval \
  --results_folder benchmarks
```

#### Using Google Models (Gemini)

```bash
python evaluation/run_eval.py \
  --backend google \
  --model_name gemini-2.0-flash-lite \
  --dataset_name leon-se/forestfire_vlm_v6_eval \
  --results_folder benchmarks/gemini
```

#### Using Self-hosted Models via vLLM

```bash
python evaluation/run_eval.py \
  --backend vllm_online \
  --vllm_url http://localhost:8000/v1 \
  --dataset_name leon-se/forestfire_vlm_v6_eval \
  --results_folder benchmarks/llava
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--backend` | VLM backend ("google", "openai", "vllm_online") | "vllm_online" |
| `--vllm_url` | URL for vLLM | "http://localhost:8000/v1" |
| `--model_name` | VLM model name | "gemini-2.0-flash-lite" |
| `--dataset_name` | Dataset name on HuggingFace | "leon-se/forestfire_vlm_v6_eval" |
| `--ds_split` | Dataset split | "train" |
| `--results_folder` | Folder to save results | "benchmarks" |


## Evaluation Output

The evaluation generates several outputs:
- CSV file containing all results
- Pickle files with model outputs
- Console output

## Citation

If you use this code in your research, please cite our paper:

```
[Citation will be added when the paper is published]
```

## License

[License information to be added]