import os
import pickle
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter

from proofread_eng.data_registry import registry as corpus_registry
from proofread_eng.proofreader import registry
from capitalization import evaluation_dataset as capitalization_dataset
from grammar import evaluation_dataset as grammar_dataset
from punctuation import evaluation_dataset as punctuation_dataset
from spelling import evaluation_dataset as spelling_dataset

eval_dict = {
    "capitalization": capitalization_dataset,
    "grammar": grammar_dataset,
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
    try:
        with open(results_path, "rb") as f:
            eval_results = pickle.load(f)
    except (FileNotFoundError, EOFError):
        eval_results = {}

    for version, proofreader in registry.items():
        if (
            (versions == "all") or (version in versions)
        ) and version not in eval_results.keys():
            if verbose:
                print(f"Evaluating proofreader {version}")
            start = time.time()
            results = run_evals(proofreader)
            eval_results[version] = results
            duration = time.time() - start
            if verbose:
                print(f"    completed in {duration:.03} seconds.")

            del proofreader

    with open(results_path, "wb") as f:
        pickle.dump(eval_results, f)

    report_results()


def run_evals(proofreader, verbose=True):
    results_dict = {}
    for eval_name, dataset in eval_dict.items():
        if verbose:
            print(f"    running {eval_name} eval")

        true_pos_total = 0
        false_pos_total = 0
        false_neg_total = 0

        for paragraph_group in dataset:
            detected_errors, _ = proofreader.proof_text(
                paragraph_group["paragraph"]
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


def report_results(
    versions="all",
    xlabel_type="version",
    debug=False,
):
    # x-axis can be labeled with proofreader version number, model name,
    # alphabet size, error threshold, training books
    # xlabel_type is one of
    #     alphabet_size
    #     error_threshold
    #     n_books
    #     version

    print(versions)
    with open(results_path, "rb") as f:
        eval_results = pickle.load(f)

    # Generate a markdown table summarizing performance
    performance_table_md = "| version |"

    categories = None
    # Find the list of evals run
    for key, val_dict in eval_results.items():
        try:
            categories = list(val_dict.keys())
            break
        except KeyError:
            # Keep cycling through the proofreader versions until one is
            # found that has results associated with it.
            pass

    if categories is None:
        print("No results found to report")
        return

    categories.sort()
    n_cols = len(categories) + 2
    for category in categories:
        performance_table_md += f" {category} |"
    performance_table_md += "\n|"
    for _ in range(n_cols):
        performance_table_md += " -------- |"

    if versions == "all":
        versions = list(eval_results.keys())
        versions.sort()

    for version in versions:
        results = eval_results[version]
        performance_table_md += f"\n| {version} |"
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
        "description",
        "model",
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

    for version in versions:
        try:
            proofreader = registry[version]
        except KeyError:
            print(f"proofreader version {version} results not found")
            continue

        n_books = 0
        try:
            for corpus_version in proofreader.model.corpus_versions:
                n_books += corpus_registry[corpus_version].n_files
        except AttributeError:
            pass
        proofreader.n_books = n_books

        model_table_md += f"\n| {version} |"
        model_table_md += f" {proofreader.model.description} |"
        model_table_md += f" {proofreader.model.version} |"
        model_table_md += f" {proofreader.model.tokenizer_version} |"
        vocab_size = proofreader.model.tokenizer.vocab_size
        if vocab_size >= 1000:
            vocab_str = f"{int(vocab_size / 1000)}k"
        else:
            vocab_str = str(int(vocab_size))
        model_table_md += f" {vocab_str} |"
        model_table_md += f" {n_books} |"
        model_table_md += f" {proofreader.error_threshold} |"
    model_table_md += "\n\nModel summaries\n"
    print(model_table_md)

    # save model_table_md to file
    with open(performance_path, "wt") as f:
        f.write(model_table_md)

    # Show performance as a line plot
    n_plot_cols = 2
    plot_width = 3
    plot_height = 3
    left_border = 1
    right_border = 0.75
    top_border = 0.75
    bottom_border = 1.25
    row_gap = 1.25
    column_gap = 1

    # Appearance
    precision_color = "#222"
    recall_color = "#444"
    tick_label_color = "#444"
    precision_linewidth = 1
    recall_linewidth = 2

    plot_dir = os.path.join(os.path.dirname(__file__), "plots")
    report_filename = f"eval_report_{int(time.time())}.png"
    report_filepath = os.path.join(plot_dir, report_filename)

    # Generate n columns x n rows of plots, one per eval
    n_plot_rows = int(np.ceil((len(categories) / n_plot_cols)))

    figure_width = (
        plot_width * n_plot_cols
        + column_gap * (n_plot_cols - 1)
        + left_border
        + right_border
    )
    figure_height = (
        plot_height * n_plot_rows
        + row_gap * (n_plot_rows - 1)
        + bottom_border
        + top_border
    )
    fig = plt.figure(figsize=(figure_width, figure_height))

    xaxis_labels = []
    for version in versions:
        try:
            proofreader = registry[version]
        except KeyError:
            continue
        if xlabel_type == "error_threshold":
            xaxis_labels.append(proofreader.error_threshold)
        elif xlabel_type == "alphabet_size":
            vocab_size = proofreader.model.tokenizer.vocab_size
            if vocab_size >= 1000:
                xaxis_labels.append(
                    f"{int(proofreader.model.tokenizer.vocab_size / 1000)}k"
                )
            else:
                xaxis_labels.append(
                    str(int(proofreader.model.tokenizer.vocab_size))
                )
        elif xlabel_type == "n_books":
            xaxis_labels.append(proofreader.n_books)
        elif xlabel_type == "version":
            xaxis_labels.append(version)
        else:
            xaxis_labels.append(version)

    for i_category, category in enumerate(categories):
        i_row = i_category // 2
        i_col = i_category % 2

        # Create axes
        left = (
            left_border + i_col * plot_width + i_col * column_gap
        ) / figure_width
        bottom = (
            bottom_border + i_row * plot_height + i_row * row_gap
        ) / figure_height
        width = plot_width / figure_width
        height = plot_height / figure_height
        ax = fig.add_axes((left, bottom, width, height))

        # For each plot, array versions along the x-axis,
        # performance on the y-axis
        precision_results = []
        recall_results = []
        for version in versions:
            precision = eval_results[version][category]["precision"]
            precision_pct = int(np.round(100 * precision))
            recall = eval_results[version][category]["recall"]
            recall_pct = int(np.round(100 * recall))
            precision_results.append(precision_pct)
            recall_results.append(recall_pct)

        # recall is solid lines, precision is dashed
        # recall and precision have distict markers
        # value labels not necessary (they're in tables)
        ax.plot(
            precision_results,
            color=precision_color,
            linestyle="--",
            linewidth=precision_linewidth,
            clip_on=False,
        )
        ax.plot(
            recall_results,
            color=recall_color,
            linestyle="-",
            linewidth=recall_linewidth,
            clip_on=False,
        )
        ax.set_ylim(0, 100)
        ax.set_xlabel(f"{xlabel_type}")
        ax.set_title(f"{category} eval")
        if i_col == 0:
            ax.set_ylabel("recall (solid), precision (dashed)")

        ax.tick_params(
            axis="x",
            labelsize=8,
            labelrotation=-90,
            labelcolor=tick_label_color,
        )
        x_formatter = FixedFormatter(xaxis_labels)
        x_locator = FixedLocator(list(range(len(versions))))
        ax.xaxis.set_major_formatter(x_formatter)
        ax.xaxis.set_major_locator(x_locator)

        ax.tick_params(
            axis="y",
            labelsize=8,
            labelrotation=0,
            labelcolor=tick_label_color,
        )

    # save to png file
    plt.show()
    fig.savefig(report_filepath, dpi=150)

    if debug:
        for proofreader in eval_results:
            print()
            print("---------------------------")
            print(proofreader["Name"])
            print()
            print(proofreader["results"])


if __name__ == "__main__":
    run_evals_for_many()
