import os

from proofread_eng.data.corpus import Corpus

data_path = os.path.dirname(__file__)

registry = {
    "00": Corpus(data_path, version="00", description="classic sci-fi novels"),
    "01": Corpus(data_path, version="01", description="classic sci-fi novels"),
    "02": Corpus(data_path, version="02", description="classic sci-fi novels"),
    "03": Corpus(data_path, version="03", description="classic sci-fi novels"),
    "04": Corpus(data_path, version="04", description="fiction books"),
    "05": Corpus(data_path, version="05", description="English texts"),
}
