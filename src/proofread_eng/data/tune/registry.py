import os

from proofread_eng.data.corpus import Corpus

data_path = os.path.dirname(__file__)

registry = {
    "100": Corpus(data_path, version="100", description="Frankenstein"),
    "101": Corpus(data_path, version="101", description="Alice in Wonderland"),
    "102": Corpus(data_path, version="102", description="Call of Cthulhu"),
}
