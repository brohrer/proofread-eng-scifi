from proofread_eng.data.tune.capitalization import evaluation_dataset as capitalization_dataset
from proofread_eng.data.tune.extra_word import evaluation_dataset as extra_word_dataset
from proofread_eng.data.tune.grammar import evaluation_dataset as grammar_dataset
from proofread_eng.data.tune.missing_word import evaluation_dataset as missing_word_dataset
from proofread_eng.data.tune.punctuation import evaluation_dataset as punctuation_dataset
from proofread_eng.data.tune.spelling import evaluation_dataset as spelling_dataset

tune_dict = {
    "capitalization": capitalization_dataset,
    "extra words": extra_word_dataset,
    "grammar": grammar_dataset,
    "missing words": missing_word_dataset,
    "punctuation": punctuation_dataset,
    "spelling": spelling_dataset,
}
