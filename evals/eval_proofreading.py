import os
import pickle
import time
import numpy as np
from proofread_eng_scifi.data_registry import registry as corpus_registry
from proofread_eng_scifi.models.fomm.registry import registry as fomm_registry
from proofread_eng_scifi.models.somm.registry import registry as somm_registry
from proofread_eng_scifi.models.random.registry import (
    registry as random_registry,
)
from proofread_eng_scifi.models.tokenizer.registry import (
    registry as tokenizer_registry,
)
from proofread_eng_scifi.registry import modules as proofreader_modules
from proofread_eng_scifi.registry import registry as proofreader_info
from capitalization import evaluation_dataset as capitalization_dataset
from punctuation import evaluation_dataset as punctuation_dataset
from spelling import evaluation_dataset as spelling_dataset

eval_dict = {
    "capitalization": capitalization_dataset,
    "punctuation": punctuation_dataset,
    "spelling": spelling_dataset,
}
models_filename = "model_summaries.md"
performance_filename = "performance_summary.md"
results_filename = "eval_results.pkl"
models_path = os.path.join(os.path.dirname(__file__), models_filename)
performance_path = os.path.join(os.path.dirname(__file__), performance_filename)
results_path = os.path.join(os.path.dirname(__file__), results_filename)


def run_evals_for_many(versions="all", verbose=True):
    for version in proofreader_info.keys():
        if (versions == "all") or (version in versions):
            run_evals_for_one(version, verbose=verbose)

    with open(results_path, "wb") as f:
        pickle.dump(proofreader_info, f)

    report_results()


def run_evals_for_one(version, verbose=True):
    proofreader = proofreader_info[version]
    if verbose:
        print(f"Evaluating proofreader {version}")
    start = time.time()
    eval_function = proofreader_modules[version].proof_text
    results = run_evals(eval_function)
    proofreader["results"] = results
    duration = time.time() - start
    if verbose:
        # print(f"    results: {results}")
        print(f"    completed in {duration:.03} seconds.")


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
        proofreader_info = pickle.load(f)

    # Generate a markdown table summarizing performance
    performance_table_md = "| version |"

    # Find the list of evals run
    for key, val_dict in proofreader_info.items():
        try:
            categories = list(val_dict["results"].keys())
            break
        except KeyError:
            # Keep cycling through the proofreader versions until one is
            # found that has results associated with it.
            pass

        print("No results found to report")
        return

    categories.sort()
    n_cols = len(categories) + 2
    for category in categories:
        performance_table_md += f" {category} |"
    performance_table_md += "\n|"
    for _ in range(n_cols):
        performance_table_md += " -------- |"

    for version, proofreader in proofreader_info.items():
        try:
            results = proofreader["results"]
        except KeyError:
            continue

        performance_table_md += f"\n| {version} |"
        # performance_table_md += f" {proofreader['description']} |"
        for category in categories:
            precision = results[category]["precision"]
            precision_pct = int(np.round(100 * precision))
            recall = results[category]["recall"]
            recall_pct = int(np.round(100 * recall))
            performance_table_md += f" ({precision_pct}) {recall_pct} |"
    performance_table_md += (
        "\n\nPerformance values are shown as: (precision %) recall %\n"
    )
    print(performance_table_md)

    # save performance_table_md to file
    with open(performance_path, "wt") as f:
        f.write(performance_table_md)

    # Generate a markdown table describing models
    columns = [
        "version",
        "model",
        "description",
        "tokenizer",
        "alphabet",
        "books",
        "error cutoff",
    ]
    model_table_md = "| "
    for col in columns:
        model_table_md += f"{col} |"
    model_table_md += "\n|"
    for _ in range(len(columns)):
        model_table_md += " -------- |"

    for version, proofreader in proofreader_info.items():
        try:
            results = proofreader["results"]
        except KeyError:
            continue

        lang_model = proofreader["model"]
        model_type, model_version = lang_model.split("_")
        if model_type == "fomm":
            model_info = fomm_registry[model_version]
        elif model_type == "somm":
            model_info = somm_registry[model_version]
        elif model_type == "random":
            model_info = random_registry[model_version]
        else:
            model_info = None
            print(
                f"model type {model_type} in proofreader "
                + f"{version} is not valid"
            )
            raise ValueError
        tokenizer_version = model_info["tokenizer_version"]
        if tokenizer_version is None:
            tokenizer_info = {}
        else:
            tokenizer_info = tokenizer_registry[tokenizer_version]

        corpuses = model_info.get("training_corpus", [])
        n_books = 0
        for corpus in corpuses:
            n_books += corpus_registry[corpus]["n_books"]

        model_table_md += f"\n| {version} |"
        model_table_md += f" {model_info['name']} |"
        model_table_md += f" {model_info['description']} |"
        model_table_md += f" {tokenizer_version} |"
        model_table_md += f" {tokenizer_info.get('alphabet_size', 0)}k |"
        model_table_md += f" {n_books} |"
        model_table_md += f" {proofreader.get('error_threshold', 'NA')} |"
    model_table_md += "\n\nModel summaries\n"
    print(model_table_md)

    # save model_table_md to file
    with open(performance_path, "wt") as f:
        f.write(model_table_md)

    # TODO: show performance as a line plot

    if debug:
        for proofreader in proofreader_info:
            print()
            print("---------------------------")
            print(proofreader["Name"])
            print()
            print(proofreader["results"])


if __name__ == "__main__":
    run_evals_for_many()
