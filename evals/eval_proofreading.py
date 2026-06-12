import os
import pickle
import time
import numpy as np
from proofread_eng_scifi.proof_01 import proof_text as proof_text_01
from proofread_eng_scifi.proof_02 import proof_text as proof_text_02
from proofread_eng_scifi.proof_03 import proof_text as proof_text_03
from proofread_eng_scifi.proof_04 import proof_text as proof_text_04
from proofread_eng_scifi.proof_05 import proof_text as proof_text_05
from proofread_eng_scifi.proof_06 import proof_text as proof_text_06
from proofread_eng_scifi.proof_07 import proof_text as proof_text_07
from proofread_eng_scifi.proof_08 import proof_text as proof_text_08
from capitalization import evaluation_dataset as capitalization_dataset
from punctuation import evaluation_dataset as punctuation_dataset
from spelling import evaluation_dataset as spelling_dataset

eval_dict = {
    "capitalization": capitalization_dataset,
    "punctuation": punctuation_dataset,
    "spelling": spelling_dataset,
}
results_filename = "eval_results.pkl"
results_path = os.path.join(os.path.dirname(__file__), results_filename)


def run_evals_for_all(verbose=True):
    proofreaders = [
        {
            "name": "proof_01",
            "lang_model": "random",
            "description": "random baseline",
            "function": proof_text_01,
            "alphabet_size": 0,
            "training_books": 0,
        },
        {
            "name": "proof_02",
            "lang_model": "FOMM_00",
            "description": "first-order Markov model",
            "function": proof_text_02,
            "alphabet_size": 20_000,
            "training_books": 10,
        },
        {
            "name": "proof_03",
            "lang_model": "SOMM_00",
            "description": "second-order Markov model",
            "function": proof_text_03,
            "alphabet_size": 20_000,
            "training_books": 10,
        },
        {
            "name": "proof_04",
            "lang_model": "FOMM_01",
            "description": "second-order Markov model",
            "function": proof_text_04,
            "alphabet_size": 20_000,
            "training_books": 20,
        },
        {
            "name": "proof_05",
            "lang_model": "SOMM_01",
            "description": "second-order Markov model",
            "function": proof_text_05,
            "alphabet_size": 1_000,
            "training_books": 20,
        },
        {
            "name": "proof_06",
            "lang_model": "SOMM_02",
            "description": "sparse second-order Markov model",
            "function": proof_text_06,
            "alphabet_size": 20_000,
            "training_books": 20,
        },
        {
            "name": "proof_07",
            "lang_model": "FOMM_02",
            "description": "sparse second-order Markov model",
            "function": proof_text_07,
            "alphabet_size": 20_000,
            "training_books": 416,
        },
        {
            "name": "proof_08",
            "lang_model": "SOMM_03",
            "description": "second-order Markov model",
            "function": proof_text_08,
            "alphabet_size": 20_000,
            "training_books": 416,
        },
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


def run_evals(proofread_text, verbose=True):
    results_dict = {}
    for eval_name, dataset in eval_dict.items():
        if verbose:
            print(f"    running {eval_name} eval")

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


def report_results(debug=False):
    with open(results_path, "rb") as f:
        proofreaders = pickle.load(f)

    # Generate a markdown table
    md_table = "| version |"
    categories = list(proofreaders[0]["results"].keys())
    categories.sort()
    n_cols = len(categories) + 2
    for category in categories:
        md_table += f" {category} |"
    md_table += "\n|"
    for _ in range(n_cols):
        md_table += " -------- |"

    for proofreader in proofreaders:
        version = proofreader["name"].split("_")[1]
        md_table += f"\n| {version} |"
        # md_table += f" {proofreader['description']} |"
        for category in categories:
            precision = proofreader["results"][category]["precision"]
            precision_pct = int(np.round(100 * precision))
            recall = proofreader["results"][category]["recall"]
            recall_pct = int(np.round(100 * recall))
            md_table += f" ({precision_pct}) {recall_pct} |"
    print()
    print(md_table)
    print()
    # TODO: save md_table to file

    # TODO: have a results table and a performance table

    # TODO: show performance as a line plot

    if debug:
        for proofreader in proofreaders:
            print()
            print("---------------------------")
            print(proofreader["name"])
            print()
            print(proofreader["results"])


if __name__ == "__main__":
    run_evals_for_all()
