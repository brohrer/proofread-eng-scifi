from os import listdir
from os.path import isfile, join
import sentencepiece as spm

data_rel_path = "../../data/proofread_eng_scifi/"
model_prefix = "m"
model_type = "unigram"  # "unigram" (default), "bpe"
normalization_rule_name = "identity"  # one of:
# nmt_nfkc: NFKC normalization with some additional normalization around spaces. (default)
# nfkc: original: NFKC normalization.
# nmt_nfkc_cf: nmt_nfkc + Unicode case folding (mostly lower casing)
# nfkc_cf: nfkc + Unicode case folding.
# identity: no normalization
remove_extra_whitespaces = False
split_by_whitespace = False
vocab_size = 20000
# Full list of argument options
# https://github.com/google/sentencepiece/blob/master/doc/options.md

python_args = True


def train():
    training_files = [
        join(data_rel_path, f)
        for f in listdir(data_rel_path)
        if isfile(join(data_rel_path, f))
    ]
    training_paths = ",".join(training_files)
    if python_args:
        spm.SentencePieceTrainer.train(
            input=training_paths,
            model_prefix=model_prefix,
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
                f"--model_prefix={model_prefix}",
                f"--model_type={model_type}",
                f"--normalization_rule_name={normalization_rule_name}",
                f"--remove_extra_whitespaces={str(remove_extra_whitespaces).lower()}",
                f"--split_by_whitespace={str(split_by_whitespace).lower()}",
                f"--vocab_size={vocab_size}",
            ]
        )
        spm.SentencePieceTrainer.train(training_arguments)

    sp = spm.SentencePieceProcessor()

    sp.load(f"{model_prefix}.model")

    # encode: text => id
    test_sentence = "This is a test of the sentencepiece tokenizer."
    test_pieces = sp.encode_as_pieces(test_sentence)
    print(test_pieces)
    test_ids = sp.encode_as_ids(test_sentence)
    print(test_ids)

    # decode: id => text
    print(sp.decode_pieces(test_pieces))
    print(sp.decode_ids([209, 31, 9, 375, 586]))
    print(sp.decode_ids(test_ids))

    shift_sentence = (
        "This is what it looks like when all the tokens in " +
        "a sentence are shifted by one."
    )
    print()
    print(shift_sentence)
    shifted_ids = [i + 1 for i in sp.encode_as_ids(shift_sentence)]
    print(sp.decode_ids(shifted_ids))
    print()

    # playing around
    # for i in range(100):
    #     print(sp.decode_ids([i]))
    # print("------------")

    for i in range(50):
        print(sp.decode_ids([i + 4000]))


if __name__ == "__main__":
    train()
