from eval_proofreading import report_results

# report_results(versions=["22", "27", "23", "28", "24", "25", "26"])
# report_results(
#     versions=["42", "53", "54", "55", "56", "57", "58", "59"],
#     xlabel_type="alphabet_size",
# )
report_results(
    versions=["60", "61", "62", "63", "64", "65", "66"],
    xlabel_type="alphabet_size",
)
