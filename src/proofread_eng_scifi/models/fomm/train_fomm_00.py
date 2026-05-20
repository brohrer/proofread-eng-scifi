import os
from proofread_eng_scifi.models.fomm.fomm import FirstOrderMarkovModel
import proofread_eng_scifi.models.tokenizer.tokenizer as tokenizer_mod

data_rel_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "data", "training"
)
model_name_for_fomm_00 = "fomm_00"
tokenizer_for_fomm_00 = "tokenizer_00"


def train(
    model_name=model_name_for_fomm_00, tokenizer_name=tokenizer_for_fomm_00
):
    tokenizer = tokenizer_mod.load(tokenizer_name)
    model = FirstOrderMarkovModel(
        n_unique_tokens=tokenizer.get_piece_size(),
        model_name=model_name,
        tokenizer_name=tokenizer_name,
    )

    training_files = [
        os.path.join(data_rel_path, f)
        for f in os.listdir(data_rel_path)
        if os.path.isfile(os.path.join(data_rel_path, f))
    ]
    for training_file in training_files:
        with open(training_file, "rt") as f:
            training_text = f.read()
            ids = tokenizer.encode_as_ids(training_text)
            model.train_from_tokens(ids)

    model.save()


if __name__ == "__main__":
    train()
