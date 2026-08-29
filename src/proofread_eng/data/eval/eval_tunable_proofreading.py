import os
import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedFormatter, FixedLocator

# TODO: create separate eval_data and make this eval.eval_data
from proofread_eng.data.tune.tuning_data import eval_dict
from proofread_eng.proofreader import registry

models_filename = "model_summaries.md"
performance_filename = "performance_summary.md"
results_filename = "eval_results.pkl"
models_path = os.path.join(os.path.dirname(__file__), models_filename)
performance_path = os.path.join(os.path.dirname(__file__), performance_filename)
results_path = os.path.join(os.path.dirname(__file__), results_filename)


def run_evals_for_many(
    versions="all",
    make_report=True,
    label_type="version",
    force_recompute=False,
    verbose=True,
):
    try:
        with open(results_path, "rb") as f:
            eval_results = pickle.load(f)
    except (FileNotFoundError, EOFError):
        eval_results = {}

    for version, proofreader in registry.items():
        if ((versions == "all") or (version in versions)) and (
            (version not in eval_results) or (force_recompute == True)
        ):
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

    if make_report:
        report_results(versions=versions, label_type=label_type)


def run_evals(proofreader, verbose=True):
    results_dict = {}
    for eval_name, dataset in eval_dict.items():
        if verbose:
            print(f"    running {eval_name} eval")

        true_pos_total = 0
        false_pos_total = 0
        true_neg_total = 0
        false_neg_total = 0

        for paragraph_group in dataset:
            detected_errors, _ = proofreader.proof_text(
                paragraph_group["paragraph"]
            )
            true_pos, false_pos, true_neg, false_neg = calculate_results(
                paragraph_group["mistakes"], detected_errors
            )
            true_pos_total += true_pos
            false_pos_total += false_pos
            true_neg_total += true_neg
            false_neg_total += false_neg

        # A small number to avoid division by zero
        epsilon = 1e-17
        precision = true_pos_total / (
            true_pos_total + false_pos_total + epsilon
        )
        # recall = true positive rate
        recall = true_pos_total / (true_pos_total + false_neg_total + epsilon)

        results_dict[eval_name] = {
            "true_pos": true_pos_total,
            "false_pos": false_pos_total,
            "true_neg": true_neg_total,
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

    # Calculate false_positives and true negatives.
    # Count all the detected errors that don't overlap at least one ground
    # truth error.
    true_negatives = 0
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
        else:
            true_negatives += 1

    return true_positives, false_positives, true_negatives, false_negatives


def report_results(
    versions="all",
    label_type="version",
    debug=False,
):
    # x-axis can be labeled with proofreader version number, model name,
    # alphabet size, error threshold, training books
    # label_type is one of
    #     alphabet_size
    #     error_threshold (alias for scaled_error_threshold)
    #     n_books
    #     version

    print(versions)
    with open(results_path, "rb") as f:
        eval_results = pickle.load(f)

    # Generate a markdown table summarizing performance
    performance_table_md = "| version |"

    categories = None
    # Find the list of evals run
    for val_dict in eval_results.values():
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

    # Summarize the proofreader and its models
    model_summaries = ""
    for version in versions:
        try:
            proofreader = registry[version]
        except KeyError:
            print(f"proofreader version {version} results not found")
            continue

        model_summaries += proofreader.stats_summary()
        for model in proofreader.models:
            model_summaries += "    " + model.stats_summary()
            model_summaries += "        " + model.tokenizer.stats_summary()

    print(model_summaries)

    with open(performance_path, "wt") as f:
        f.write(model_summaries)

    # Show performance as a line plot
    n_plot_cols = 3
    plot_width = 2.3
    plot_height = 2.3
    left_border = 1
    right_border = 0.70
    top_border = 0.65
    bottom_border = 1
    row_gap = 1
    column_gap = 1

    # Appearance
    precision_color = "#222"
    recall_color = "#444"
    pr_curve_color = "#444"
    label_color = "#444"
    precision_linewidth = 1
    recall_linewidth = 2
    pr_curve_linewidth = 2
    label_fontsize = 7

    plot_dir = os.path.join(os.path.dirname(__file__), "plots")
    report_filename = f"eval_report_{int(time.time())}.png"
    report_filepath = os.path.join(plot_dir, report_filename)

    # Generate n columns x n rows of plots, one per eval
    n_plot_rows = int(np.ceil(len(categories) / n_plot_cols))

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
    fig_horiz = plt.figure(figsize=(figure_width, figure_height))

    performance_point_labels = []
    for version in versions:
        try:
            proofreader = registry[version]
        except KeyError:
            continue
        if label_type == "error_threshold":
            performance_point_labels.append(proofreader.scaled_error_threshold)
        elif label_type == "alphabet_size":
            try:
                vocab_size = proofreader.model.tokenizer.vocab_size
            except AttributeError:
                vocab_size = proofreader.models[0].tokenizer.vocab_size
            if vocab_size >= 1000:
                performance_point_labels.append(f"{int(vocab_size / 1000)}k")
            else:
                performance_point_labels.append(str(int(vocab_size)))

        elif label_type == "n_books":
            performance_point_labels.append(proofreader.n_books)
        elif label_type == "version":
            performance_point_labels.append(version)
        else:
            raise ValueError(f"label_type not valid: {label_type}")

    precision_results = {}
    recall_results = {}

    for i_category, category in enumerate(categories):
        i_row = n_plot_rows - i_category // n_plot_cols - 1
        i_col = i_category % n_plot_cols

        precision_results[category] = []
        recall_results[category] = []

        for version in versions:
            results = eval_results[version]

            precision = results[category]["precision"]
            precision_pct = int(np.round(100 * precision))
            precision_results[category].append(precision_pct)

            recall = results[category]["recall"]
            recall_pct = int(np.round(100 * recall))
            recall_results[category].append(recall_pct)

        # Create axes
        left = (
            left_border + i_col * plot_width + i_col * column_gap
        ) / figure_width
        bottom = (
            bottom_border + i_row * plot_height + i_row * row_gap
        ) / figure_height
        width = plot_width / figure_width
        height = plot_height / figure_height
        ax = fig_horiz.add_axes((left, bottom, width, height))

        # For each plot, array versions along the x-axis,
        # performance on the y-axis

        # recall is solid lines, precision is dashed
        # recall and precision have distict markers
        # value labels not necessary (they're in tables)
        ax.plot(
            precision_results[category],
            color=precision_color,
            linestyle="--",
            linewidth=precision_linewidth,
            clip_on=False,
        )
        ax.plot(
            recall_results[category],
            color=recall_color,
            linestyle="-",
            linewidth=recall_linewidth,
            clip_on=False,
        )
        ax.set_ylim(0, 100)
        ax.set_xlabel(f"{label_type}")
        ax.set_title(f"{category} eval")
        if i_col == 0:
            ax.set_ylabel("recall (solid), precision (dashed)")

        ax.tick_params(
            axis="x",
            labelsize=label_fontsize,
            labelrotation=-90,
            labelcolor=label_color,
        )
        x_formatter = FixedFormatter(performance_point_labels)
        x_locator = FixedLocator(list(range(len(versions))))
        ax.xaxis.set_major_formatter(x_formatter)
        ax.xaxis.set_major_locator(x_locator)

        ax.tick_params(
            axis="y",
            labelsize=label_fontsize,
            labelrotation=0,
            labelcolor=label_color,
        )

    # save to png file
    fig_horiz.savefig(report_filepath, dpi=150)

    # Create receiver-operator curve (ROC) plots
    report_filename = f"eval_report_pr_{int(time.time())}.png"
    report_filepath = os.path.join(plot_dir, report_filename)

    fig_prec_rec = plt.figure(figsize=(figure_width, figure_height))
    max_auc = 0
    min_auc = 1

    for i_category, category in enumerate(categories):
        i_row = n_plot_rows - i_category // n_plot_cols - 1
        i_col = i_category % n_plot_cols

        # Create axes
        left = (
            left_border + i_col * plot_width + i_col * column_gap
        ) / figure_width
        bottom = (
            bottom_border + i_row * plot_height + i_row * row_gap
        ) / figure_height
        width = plot_width / figure_width
        height = plot_height / figure_height
        ax = fig_prec_rec.add_axes((left, bottom, width, height))

        ax.plot(
            recall_results[category],
            precision_results[category],
            color=pr_curve_color,
            linestyle="-",
            linewidth=pr_curve_linewidth,
            marker=".",
            clip_on=False,
        )

        xlabel_offset = 2
        ylabel_offset = 0.5
        for i_point, (prec, rec) in enumerate(
            zip(precision_results[category], recall_results[category])
        ):
            ax.text(
                min(rec + xlabel_offset, 86),
                min(prec + ylabel_offset, 93),
                performance_point_labels[i_point],
                fontsize=label_fontsize,
                color=label_color,
                horizontalalignment="left",
                verticalalignment="bottom",
            )

        # Calculate the area under the precision-recall curve (AUPRC)
        # by summing trapezoids
        auc = 0.0
        for i_trap in range(len(recall_results[category]) - 1):
            width = abs(
                recall_results[category][i_trap]
                - recall_results[category][i_trap + 1]
            )
            height = (
                precision_results[category][i_trap]
                + precision_results[category][i_trap + 1]
            ) / 2.0
            auc += width * height / 10000

        max_auc = max(max_auc, auc)
        min_auc = min(min_auc, auc)

        # Add some text in the upper-right corner
        ax.text(
            100 - xlabel_offset,
            100 - ylabel_offset,
            (
                f"Area under curve = {auc:.3f}\n"
                + f"with {' '.join(label_type.split('_'))}"
            ),
            fontsize=label_fontsize,
            color=label_color,
            horizontalalignment="right",
            verticalalignment="top",
        )

        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_title(f"{category} eval")
        if i_row == 0:
            ax.set_xlabel("Recall")
        if i_col == 0:
            ax.set_ylabel("Precision")

    print(f"AUC range: {min_auc:.2f} - {max_auc:.2f}")

    # save to png file
    plt.show()
    fig_prec_rec.savefig(report_filepath, dpi=150)

    if debug:
        for proofreader in eval_results:
            print()
            print("---------------------------")
            print(proofreader["Name"])
            print()
            print(proofreader["results"])


if __name__ == "__main__":
    run_evals_for_many()
