import os
from proofread_eng_scifi.models.somm.somm_sparse import (
    SparseSecondOrderMarkovModel as Model,
)
import proofread_eng_scifi.models.tokenizer.tokenizer as tokenizer_mod

MODEL_NAME = "somm_03"
TOKENIZER_NAME = "tokenizer_05"

training_data_top = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "..",
    "data",
)
training_data_dirs = [
    "training_02",
]
error_threshold = 1e-8


def train(
    model_name=MODEL_NAME,
    tokenizer_name=TOKENIZER_NAME,
    verbose=True,
):
    tokenizer = tokenizer_mod.load(tokenizer_name)
    model = Model(
        n_unique_tokens=tokenizer.get_piece_size(),
        model_name=model_name,
        tokenizer_name=tokenizer_name,
        error_threshold=error_threshold,
    )

    if verbose:
        print()
        print("Training...")
    for training_data_dir in training_data_dirs:
        data_rel_path = os.path.join(training_data_top, training_data_dir)
        training_files = [
            os.path.join(data_rel_path, f)
            for f in os.listdir(data_rel_path)
            if os.path.isfile(os.path.join(data_rel_path, f))
        ]
        for training_file in training_files:
            with open(training_file, "rt") as f:
                filename = training_file.split(os.pathsep)[-1]
                try:
                    training_text = f.read()
                except UnicodeDecodeError:
                    print(
                        "UnicodeDecodeError encountered, "
                        + f"skipping {training_file}"
                    )
                    continue

                if verbose:
                    print(f"    {filename}")
                ids = tokenizer.encode_as_ids(training_text)
                model.train_from_tokens(ids)

    model.save()


if __name__ == "__main__":
    train()
