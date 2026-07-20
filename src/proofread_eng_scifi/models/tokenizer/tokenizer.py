import os
import sentencepiece as spm
from proofread_eng_scifi.data_registry import registry as data_registry


class Tokenizer:
    """
    training argument details:
    https://github.com/google/sentencepiece/blob/master/doc/options.md
    """

    def __init__(
        self,
        version=None,  # tokenizer_version
        corpus_version=None,
        vocab_size=None,  # number of unique tokens
        model_type="unigram",  # "unigram" or "bpe"
        normalization_rule_name="identity",
        # normalization_rule_name is one of:
        # identity: no normalization
        # nfkc: original: NFKC normalization.
        # nmt_nfkc: NFKC normalization with some additional
        #     normalization around spaces.
        # nmt_nfkc_cf: nmt_nfkc + Unicode case folding (mostly lower casing)
        # nfkc_cf: nfkc + Unicode case folding.
        remove_extra_whitespaces=False,
        split_by_whitespace=False,
        model_dir=os.path.dirname(__file__),
    ):
        self.version = version
        self.corpus_version = corpus_version
        self.vocab_size = vocab_size
        self.model_type = model_type
        self.normalization_rule_name = normalization_rule_name
        self.remove_extra_whitespaces = remove_extra_whitespaces
        self.split_by_whitespace = split_by_whitespace

        self.model_filename = self.version + ".model"
        self.model_dir = model_dir
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.model = None

        # Check whether the trained model exists
        # If not, train it
        if not os.path.isfile(self.model_path):
            self.train()

    def train(self):
        """
        The train() call below is a wrapper around the command line
        invocation:

        training_arguments = " ".join(
            [
                f"--input={training_paths}",
                f"--model_prefix={self.version}",
                f"--model_type={elf.odel_type}",
                f"--normalization_rule_name={self.normalization_rule_name}",
                f"--remove_extra_whitespaces={str(self.remove_extra_whitespaces).lower()}",
                f"--split_by_whitespace={str(self.split_by_whitespace).lower()}",
                f"--vocab_size={self.vocab_size}",
            ]
        )
        spm.SentencePieceTrainer.train(training_arguments)
        """
        training_corpus = data_registry[self.corpus_version]
        training_paths = ",".join(training_corpus.get_filepaths_list())
        spm.SentencePieceTrainer.train(
            input=training_paths,
            model_prefix=os.path.join(self.model_dir, self.version),
            model_type=self.model_type,
            normalization_rule_name=self.normalization_rule_name,
            remove_extra_whitespaces=self.remove_extra_whitespaces,
            split_by_whitespace=self.split_by_whitespace,
            vocab_size=self.vocab_size,
        )

    def load(self):
        self.model = spm.SentencePieceProcessor()
        self.model.load(self.model_path)

    def encode_as_ids(self, body):
        if self.model is None:
            self.load()
        return self.model.encode_as_ids(body)

    def encode_as_pieces(self, body):
        if self.model is None:
            self.load()
        return self.model.encode_as_pieces(body)

    def decode_ids(self, body):
        if self.model is None:
            self.load()
        return self.model.decode_ids(body)

    def decode_pieces(self, body):
        if self.model is None:
            self.load()
        return self.model.decode_pieces(body)

    def get_piece_size(self):
        if self.model is None:
            self.load()
        return self.model.get_piece_size()


registry = {
    "00": Tokenizer(version="00", corpus_version="00", vocab_size=20000),
    "01": Tokenizer(version="01", corpus_version="00", vocab_size=10000),
    "02": Tokenizer(version="02", corpus_version="00", vocab_size=5000),
    "03": Tokenizer(version="03", corpus_version="00", vocab_size=2000),
    "04": Tokenizer(version="04", corpus_version="00", vocab_size=1000),
    "05": Tokenizer(version="05", corpus_version="02", vocab_size=20000),
    "06": Tokenizer(version="06", corpus_version="02", vocab_size=10000),
    "07": Tokenizer(version="07", corpus_version="02", vocab_size=5000),
    "08": Tokenizer(version="08", corpus_version="02", vocab_size=2000),
    "09": Tokenizer(version="09", corpus_version="02", vocab_size=1000),
    "10": Tokenizer(version="10", corpus_version="100", vocab_size=100),
    "11": Tokenizer(version="11", corpus_version="02", vocab_size=500),
    "12": Tokenizer(version="12", corpus_version="02", vocab_size=200),
    "13": Tokenizer(version="13", corpus_version="02", vocab_size=100),
}
