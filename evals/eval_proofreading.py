from proofread_eng_scifi.proof_01 import proof_text as proof_text_01
from spelling import evaluation_dataset as spelling_dataset

eval_dict = {
    "spelling": spelling_dataset,
}


def run_evals():
    results_dict = {}
    for eval_name, dataset in eval_dict.items():
        true_pos_total = 0
        false_pos_total = 0
        false_neg_total = 0

        for paragraph_group in dataset:
            detected_errors, _ = proof_text_01(paragraph_group["paragraph"])
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

    print(results_dict)


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


if __name__ == "__main__":
    run_evals()
