from eval_tunable_proofreading import run_evals_for_many

versions = [
    "000",
]


run_evals_for_many(
    versions=versions,
    force_recompute=True,
    # label_type="alphabet_size",
    label_type="scaled_error_threshold",
    verbose=False,
)
