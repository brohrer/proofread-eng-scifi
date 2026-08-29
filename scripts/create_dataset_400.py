# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
# ]
# ///

"""
Run from the directory with
    uv run create_dataset_1k.py
"""

import os

import pandas as pd

# import the csv of metadata
metadata_file = "../metadata/metadata.csv"
gut_df = pd.read_csv(metadata_file)

# filter to all English language items
en_df = gut_df.loc[gut_df.loc[:, "language"].str.contains("en"), :]

# identify all topics with "science fiction" in the name
sf_df = en_df.loc[en_df.loc[:, "subjects"].str.contains("Science fiction"), :]

# filter to text items
tx_df = sf_df.loc[sf_df.loc[:, "type"].str.contains("Text"), :]

# remove evaluation texts
evaluation_texts = [
    "frankenstein",
    "cthulhu",
    "alice's adventures",
]
for evaluation_text in evaluation_texts:
    tx_df = tx_df.loc[
        ~tx_df.loc[:, "title"].str.lower().str.contains(evaluation_text), :
    ]

print(tx_df)

# select a subset of 1k

# save to training data directory
training_dir = "training_texts"
os.makedirs(training_dir, exist_ok=True)
files_added = 0
files_skipped = 0

for file_id in tx_df["id"]:
    filename = file_id + "_raw.txt"
    source = os.path.join("..", "data", "raw", filename)
    target = os.path.join(training_dir, filename)

    print(file_id)
    # clean out front- and end-matter
    try:
        with open(source, "rt") as f:
            text = f.read()
    except UnicodeDecodeError:
        print("UnicodeDecodeError. Moving on.")
        files_skipped += 1
        continue
    except FileNotFoundError:
        # print("FileNotFoundError. Moving on.")
        files_skipped += 1
        continue

    # find start index
    try:
        header_start = text.index("*** START OF")
        header_end = text[header_start + 1 :].index("***\n") + header_start + 5
    except ValueError:
        header_start = text.index("***START OF")
        header_end = text[header_start + 1 :].index("***\n") + header_start + 4
    print(text[header_start:header_end])

    # find end index
    try:
        footer_start = text.index("End of the Project Gutenberg")
    except ValueError:
        try:
            footer_start = text.index("*** END OF")
        except ValueError:
            footer_start = text.index("***END OF")
    print(text[footer_start : footer_start + 30])

    with open(target, "wt") as f:
        f.write(text[header_end:footer_start])
    files_added += 1

print(f"{files_added} files added,  {files_skipped} files skipped")
