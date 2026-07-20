import os
from proofread_eng_scifi.data_registry import Corpus, data_path, registry


def test_registry_loading():
    assert isinstance(registry, dict)
    assert isinstance(list(registry.keys())[0], str)
    assert isinstance(list(registry.values())[0], Corpus)
    assert len(list(registry.keys())) > 3
    assert registry["100"].description == "Frankenstein"


def test_data_path():
    data_dirs = os.listdir(data_path)
    assert len(data_dirs) > 5
    assert "00" in data_dirs
    assert "05" in data_dirs
    assert "101" in data_dirs
    assert "-1" not in data_dirs


def test_corpus():
    data_corpus = Corpus(version="01", description="a test corpus")

    assert data_corpus.path[-2:] == "01"
    assert data_corpus.n_files == 10
    assert data_corpus.description == "a test corpus"
    assert len(os.listdir(data_corpus.path)) == 10
    assert len(data_corpus.get_filenames_list()) == 10
    assert len(data_corpus.get_filepaths_list()) == 10
    assert len(list(data_corpus.get_text_files())) == 10
