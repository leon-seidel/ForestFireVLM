import os
import pickle
import json
import csv
from tqdm import tqdm
from sklearn.metrics import confusion_matrix
from templates.answer_schema import smoke_detection_schema

def eval_structured_data(predictions_text, ground_truth_dicts, vlm_name, dataset_name, 
                         write_to_file=True, results_folder='benchmarks', confusion_keys=[]):
    # Check if predictions and ground truth have the same length
    if len(predictions_text) != len(ground_truth_dicts):
        raise ValueError("Predictions and ground truth have different lengths")
    
    # Initialize length of results and count of incorrect structured outputs
    results_len = len(ground_truth_dicts)
    structured_output_incorrect = 0

    # Initialize results dictionaries
    results_abs, results_rel = {}, {}
    for key in ground_truth_dicts[0].keys():
        results_abs[key] = 0
        results_rel[key] = 0.0

    # Initialize confusion dictionaries
    bool_dicts, confusion_evals = {}, {}
    for confusion_key in confusion_keys:
        bool_dicts[confusion_key] = {"gt_bools": [], "pred_bools": []}

    for pred_text, gt_dict in zip(predictions_text, ground_truth_dicts):
        # Remove code block markdown if present
        pred_text = pred_text.lstrip("```json").rstrip("```")
        
        # Check if structured output is correct
        try:
            pred_dict = json.loads(pred_text)
            # Check if prediction is correct
            for key in gt_dict.keys():
                if gt_dict[key] == pred_dict[key]:
                    results_abs[key] += 1
            # Check confusion keys
            for confusion_key in confusion_keys:
                gt_bool = True if gt_dict[confusion_key] == "Yes" else False
                pred_bool = True if pred_dict[confusion_key] == "Yes" else False
                bool_dicts[confusion_key]["gt_bools"].append(gt_bool)
                bool_dicts[confusion_key]["pred_bools"].append(pred_bool)
        except Exception as e:
            print(e)
            structured_output_incorrect += 1
            continue
    
    # Calculate relative results
    for key in results_abs.keys():
        results_rel[key] = round(results_abs[key] / results_len, 4)
    
    # Calculate overall accuracy
    results_rel["overall_score"] = round(sum(results_rel.values()) / len(results_rel), 4)
    results_rel["structured_output_correct_ratio"] = round((results_len - structured_output_incorrect) / results_len, 4)

    # Calculate confusion metrics
    for confusion_key in confusion_keys:
        cm = confusion_matrix(bool_dicts[confusion_key]["gt_bools"], bool_dicts[confusion_key]["pred_bools"])
        tn, fp, fn, tp = cm.ravel()
        accuracy = round((tp + tn) / (tp + tn + fp + fn), 4)
        precision = round(tp / (tp + fp), 4)
        recall = round(tp / (tp + fn), 4)
        f1_score = round(2 * (precision * recall) / (precision + recall), 4)
        confusion_evals[confusion_key] = {"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1_score}
        results_rel[f"confusion_{confusion_key}"] = confusion_evals

    # Print results
    print(f"\n\nResults for {vlm_name} on {dataset_name}:\n")
    for key, value in results_rel.items():
        print(f"{key}: {value}")

    # Write results to files
    if write_to_file:
        vlm_name_str = vlm_name.replace("/", "-")
        dataset_name_str = dataset_name.replace("/", "-")

        # Create folders if they don't exist
        benchmark_folder_ds = f"{results_folder}/{dataset_name_str}"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        if not os.path.exists(benchmark_folder_ds):
            os.makedirs(benchmark_folder_ds)

        write_eval_to_list(results_rel, vlm_name_str, folder=benchmark_folder_ds)
        write_eval_to_file(results_rel, vlm_name_str, dataset_name_str, predictions_text, ground_truth_dicts, 
                           folder=benchmark_folder_ds)

    return results_rel


def write_eval_to_list(results_rel, vlm_name, folder):
    # Open file in append mode
    filename = f"{folder}/eval_results.csv"

    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as f:
            pass

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        
        # Write header if file is empty
        f.seek(0, 2)  # Go to end of file
        if f.tell() == 0:  # If file is empty, write header
            header = ['model'] + list(results_rel.keys())
            writer.writerow(header)
            
        # Write results
        row = [vlm_name] + list(results_rel.values())
        writer.writerow(row)
    
    print(f"\nResults list {filename} updated")


def write_eval_to_file(results_rel, vlm_name, dataset_name, predictions_text, ground_truth_dicts, folder):
    # Save full results to file       
    full_results = {
        "model_name": vlm_name,
        "dataset_name": dataset_name,
        "results": results_rel,
        "predictions_text": predictions_text,
        "ground_truth_dicts": ground_truth_dicts
        }

    filename = f"{folder}/{vlm_name}.pkl"
    with open(filename, 'wb') as f:
        pickle.dump(full_results, f)

    print(f"Full results saved to {filename}")


def open_eval_file(filename):
    """Open evaluation file and return model name, dataset name, results dictionary, predictions text and ground truth dictionaries"""
    with open(filename, 'rb') as f:
        full_results = pickle.load(f)
        model_name = full_results["model_name"]
        dataset_name = full_results["dataset_name"]
        results = full_results["results"]
        predictions_text = full_results["predictions_text"]
        ground_truth_dicts = full_results["ground_truth_dicts"]
        return model_name, dataset_name, results, predictions_text, ground_truth_dicts


def create_predictions(eval_ds, vlm):
    ground_truth_dicts = []
    predictions_text = []

    print(f"\nDataset size: {len(eval_ds)}\nModel: {vlm.model_name}\n")
    # Iterate over the dataset
    for sample in tqdm(eval_ds):
        image = sample["image"]
        prompt = sample["prompt"]
        gt_dict = sample["gt_dict"]
        response_schema = smoke_detection_schema
        vlm_prediction = vlm.generate_structured_response_from_pil_image(prompt, image, response_schema)
        ground_truth_dicts.append(gt_dict)
        predictions_text.append(vlm_prediction)
    
    return predictions_text, ground_truth_dicts


def create_predictions_batched(eval_ds, vlm):
    # Create predictions for the dataset
    images = []
    prompts = []
    ground_truth_dicts = []
    response_schema = smoke_detection_schema

    print(f"Dataset size: {len(eval_ds)}\nModel: {vlm.model_name}\n")
    # Iterate over the dataset
    for sample in eval_ds:
        images.append(sample["image"])
        prompts.append(sample["prompt"])
        ground_truth_dicts.append(sample["gt_dict"])

    predictions_text = vlm.generate_structured_response_from_pil_image_batch(prompts, images, response_schema)

    return predictions_text, ground_truth_dicts
