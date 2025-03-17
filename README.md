# ForestFireVLM

ForestFireVLM is a framework for evaluating Vision Language Models (VLMs) on forest fire detection and analysis tasks. The framework provides structured evaluation methods to assess how well different VLMs can identify smoke, flames, fire characteristics, and potential hazards from aerial imagery.

## About the paper

*This section will be updated when the paper is published.*

This code accompanies a research paper currently under peer review with MDPI. The paper explores the application of Vision Language Models for automated forest fire detection and analysis from aerial imagery.

**Links:**
- Paper: [Link to be added upon publication]
- Models and Dataset Collection: [HuggingFace](https://huggingface.co/collections/leon-se/forestfirevlm-67d3429a77d9a5fc6c7ce9f5)

## Setup

```bash
# Clone the repository
git clone https://github.com/leon-se/ForestFireVLM
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
python run_eval.py \
  --backend openai \
  --model_name gpt-4o \
  --dataset_name leon-se/ForestFireInsights-Eval \
  --results_folder benchmarks
```

#### Using Google Models (Gemini)

```bash
python run_eval.py \
  --backend google \
  --model_name gemini-2.0-flash-lite \
  --dataset_name leon-se/ForestFireInsights-Eval \
  --results_folder benchmarks
```

#### Using Self-hosted Models via vLLM

```bash
python run_eval.py \
  --backend vllm_online \
  --vllm_url http://localhost:8000/v1 \
  --dataset_name leon-se/ForestFireInsights-Eval \
  --results_folder benchmarks
```

### Analyzing Single Images

For quick analysis of individual images, use `run_single_image.py`:

```bash
# Analyze a local image file
python run_single_image.py \
  --backend openai \
  --model_name gpt-4o \
  --image path/to/your/image.jpg

# Analyze an image from a URL
python run_single_image.py \
  --backend google \
  --model_name gemini-2.0-flash-lite \
  --image https://example.com/forest_fire_image.jpg

# Using a self-hosted model
python run_single_image.py \
  --backend vllm_online \
  --vllm_url http://localhost:8000/v1 \
  --image path/to/your/image.jpg
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--backend` | VLM backend ("google", "openai", "vllm_online") | "vllm_online" |
| `--vllm_url` | URL for vLLM | "http://localhost:8000/v1" |
| `--model_name` | VLM model name | "gemini-2.0-flash-lite" |
| `--dataset_name` | Dataset name on HuggingFace | "leon-se/ForestFireInsights-Eval" |
| `--ds_split` | Dataset split | "train" |
| `--results_folder` | Folder to save results | "benchmarks" |
| `--image` | Path to local image or image URL (for run_single_image.py) | None |


## Batch evaluation
The notebook `batch_evaluation.ipynb` allows batched evaluation for all backends with a custom number of workers and a preliminary JSONL file.

## Evaluation Output

The evaluation generates several outputs:
- CSV file containing all results
- Pickle files with model outputs
- Console output

## Benchmark results
All raw results and Pickle files can be found in the `benchmarks` folder. The predictions can be obtained from a pickle file with the following code:

```py
from evaluation.forestfire_evaluation import open_eval_file
eval_file = 'benchmarks/leon-se-figlib-test/leon-se-ForestFireVLM-7B.pkl'
model_name, dataset_name, results, predictions_text, ground_truth_dicts = open_eval_file(eval_file)
```

Disclaimer: We changed the names of both the models and datasets before publication. Some of the Pickle files therefore have a different `model_name` or `dataset_name` saved with them.

## Citation

If you use this code in your research, please cite our paper:

```
[Citation will be added when the paper is published]
```
