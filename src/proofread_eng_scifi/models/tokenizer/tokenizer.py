import os
import sentencepiece as spm

default_data_rel_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "data", "training"
)
default_model_name = "tokenizer_no_9"

default_normalization_rule_name = "identity"  # one of:
# nmt_nfkc: NFKC normalization with some additional normalization around spaces. (default)
# nfkc: original: NFKC normalization.
# nmt_nfkc_cf: nmt_nfkc + Unicode case folding (mostly lower casing)
# nfkc_cf: nfkc + Unicode case folding.
# identity: no normalization


def train(
    data_rel_path=default_data_rel_path,
    model_name=default_model_name,
    model_type="unigram",  # "unigram" or "bpe"
    normalization_rule_name=default_normalization_rule_name,
    remove_extra_whitespaces=False,
    split_by_whitespace=False,
    vocab_size=20000,
    python_args=True,
):
    model_path_prefix = os.path.join(os.path.dirname(__file__), model_name)
    training_files = [
        os.path.join(data_rel_path, f)
        for f in os.listdir(data_rel_path)
        if os.path.isfile(os.path.join(data_rel_path, f))
    ]
    training_paths = ",".join(training_files)
    if python_args:
        spm.SentencePieceTrainer.train(
            input=training_paths,
            model_prefix=model_path_prefix,
            model_type=model_type,
            normalization_rule_name=normalization_rule_name,
            remove_extra_whitespaces=remove_extra_whitespaces,
            split_by_whitespace=split_by_whitespace,
            vocab_size=vocab_size,
        )
    else:
        training_arguments = " ".join(
            [
                f"--input={training_paths}",
                f"--model_prefix={model_path_prefix}",
                f"--model_type={model_type}",
                f"--normalization_rule_name={normalization_rule_name}",
                f"--remove_extra_whitespaces={str(remove_extra_whitespaces).lower()}",
                f"--split_by_whitespace={str(split_by_whitespace).lower()}",
                f"--vocab_size={vocab_size}",
            ]
        )
        spm.SentencePieceTrainer.train(training_arguments)

    return spm.SentencePieceProcessor()


def load(model_name):
    """
    model_name: str
    The nameof the model, minus the .model suffix.
    """
    model_filename = model_name + ".model"
    model_path = os.path.join(os.path.dirname(__file__), model_filename)
    tokenizer = spm.SentencePieceProcessor()
    tokenizer.load(model_path)
    return tokenizer


if __name__ == "__main__":
    train()
