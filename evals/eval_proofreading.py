import os
import pickle
import time
import numpy as np
from proofread_eng_scifi.proof_01 import proof_text as proof_text_01
from proofread_eng_scifi.proof_02 import proof_text as proof_text_02
from capitalization import evaluation_dataset as capitalization_dataset
from spelling import evaluation_dataset as spelling_dataset

eval_dict = {
    "spelling": spelling_dataset,
    "capitalization": capitalization_dataset,
}
results_filename = "eval_results.pkl"
results_path = os.path.join(os.path.dirname(__file__), results_filename)


def run_evals_for_all(verbose=True):
    proofreaders = [
        {
            "name": "proof_01",
            "description": "random",
            "function": proof_text_01,
        },
        {
            "name": "proof_02",
            "description": "FOMM",
            "function": proof_text_02,
        }
    ]
    for proofreader in proofreaders:
        if verbose:
            print(f"Evaluating proofreader {proofreader['name']}")
        start = time.time()
        proofreader["results"] = run_evals(proofreader["function"])
        duration = time.time() - start
        if verbose:
            print(f"    completed in {duration:.03} seconds.")

    with open(results_path, "wb") as f:
        pickle.dump(proofreaders, f)

    report_results()


def run_evals(proofread_text):
    results_dict = {}
    for eval_name, dataset in eval_dict.items():
        true_pos_total = 0
        false_pos_total = 0
        false_neg_total = 0

        for paragraph_group in dataset:
            detected_errors, _ = proofread_text(
                paragraph_group["paragraph"],
                verbose=False,
            )
            true_pos, false_pos, false_neg = calculate_results(
                paragraph_group["mistakes"], detected_errors
            )
            true_pos_total += true_pos
            false_pos_total += false_pos
            false_neg_total += false_neg
        precision = true_pos_total / (true_pos_total + false_pos_total)
        recall = true_pos_total / (true_pos_total + false_neg_total)

        results_dict[eval_name] = {
            "true_pos": true_pos_total,
            "false_pos": false_pos_total,
            "false_neg": false_neg_total,
            "precision": precision,
            "recall": recall,
        }

    return results_dict


def calculate_results(ground_truth, detected):
    # Calculate true positives and false negatives.
    # Count all the ground truth errors that are overlapped by at least one
    # detected error and those that are not.
    true_positives = 0
    false_negatives = 0
    for err in ground_truth:
        ground_truth_detected = False
        for det in detected:
            if (
                det["first_char"] <= err["last_char"]
                and det["last_char"] >= err["first_char"]
            ):
                ground_truth_detected = True
        if ground_truth_detected:
            true_positives += 1
        else:
            false_negatives += 1

    # Calculate false_positives.
    # Count all the detected errors that don't overlap at least one ground
    # truth error.
    false_positives = 0
    for det in detected:
        detection_miss = True
        for err in ground_truth:
            if (
                det["first_char"] <= err["last_char"]
                and det["last_char"] >= err["first_char"]
            ):
                detection_miss = False
        if detection_miss:
            false_positives += 1

    return true_positives, false_positives, false_negatives


def report_results():
    with open(results_path, "rb") as f:
        proofreaders = pickle.load(f)

    n_evals = len(proofreaders)
    n_cols = n_evals + 1
    n_rows = len(proofreaders)

    # Generate a markdown table
    md_table = "| model | name |"
    categories = list(proofreaders[0]["results"].keys())
    categories.sort()
    for category in categories:
        md_table += f" {category} |"
    md_table += "\n|"
    for _ in range(n_cols):
        md_table += " -------- |"

    for proofreader in proofreaders:
        md_table += f"\n| {proofreader['description']} |"
        md_table += f"{proofreader['name']} |"
        for category in categories:
            precision = proofreader["results"][category]["precision"]
            precision_pct = int(np.round(100 * precision))
            recall = proofreader["results"][category]["recall"]
            recall_pct = int(np.round(100 * recall))
            md_table += f" ({precision_pct}) {recall_pct} |"
    print(md_table)

    for proofreader in proofreaders:
        print()
        print("---------------------------")
        print(proofreader["name"])
        print()
        print(proofreader["results"])


if __name__ == "__main__":
    run_evals_for_all()
