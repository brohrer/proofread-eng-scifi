from proofread_eng.data.eval.capitalization import evaluation_dataset as capitalization_dataset
from proofread_eng.data.eval.extra_word import evaluation_dataset as extra_word_dataset
from proofread_eng.data.eval.grammar import evaluation_dataset as grammar_dataset
from proofread_eng.data.eval.missing_word import evaluation_dataset as missing_word_dataset
from proofread_eng.data.eval.punctuation import evaluation_dataset as punctuation_dataset
from proofread_eng.data.eval.spelling import evaluation_dataset as spelling_dataset

eval_dict = {
    "capitalization": capitalization_dataset,
    "extra words": extra_word_dataset,
    "grammar": grammar_dataset,
    "missing words": missing_word_dataset,
    "punctuation": punctuation_dataset,
    "spelling": spelling_dataset,
}
