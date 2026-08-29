from eval_proofreading import run_evals_for_many

versions = [
    "414",
]


run_evals_for_many(
    versions=versions,
    force_recompute=True,
    # label_type="alphabet_size",
    # label_type="beta",
    # label_type="error_threshold",
    label_type="scaled_error_threshold",
    verbose=False,
)
