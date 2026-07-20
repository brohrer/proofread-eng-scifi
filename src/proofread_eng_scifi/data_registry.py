import os

data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data")


class Corpus:
    """
    Provide a convenient way to access the training and evaluation texts.
    Models should not have to worry about paths and reading files.
    """

    def __init__(self, version=None, description=""):
        self.path = os.path.join(data_path, version)
        self.n_files = len(self.get_filenames_list())
        self.description = description

    def get_filenames_list(self):
        filenames = []
        for filename in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, filename)):
                filenames.append(filename)
        return filenames

    def get_filepaths_list(self):
        paths = []
        for filename in self.get_filenames_list():
            paths.append(os.path.join(self.path, filename))
        return paths

    def get_text_files(self, verbose=False):
        """
        An iterator that gives the full text of each file as a single string.
        """
        i_file = 0
        for filepath in self.get_filepaths_list():
            with open(filepath, "rt") as f:
                try:
                    file_text = f.read()
                except UnicodeDecodeError:
                    print(
                        "UnicodeDecodeError encountered, "
                        + f"skipping {filepath}"
                    )
                    continue
                if verbose:
                    i_file += 1
                    filename = filepath.split(os.path.sep)[-1]
                    print(
                        f"    reading file {i_file} of {self.n_files}: {filename}"
                    )
            yield file_text

            del file_text


registry = {
    "00": Corpus(version="00", description="classic sci-fi novels"),
    "01": Corpus(version="01", description="classic sci-fi novels"),
    "02": Corpus(version="02", description="classic sci-fi novels"),
    "03": Corpus(version="03", description="classic sci-fi novels"),
    "04": Corpus(version="04", description="fiction books"),
    "05": Corpus(version="05", description="English texts"),
    "100": Corpus(version="100", description="Frankenstein"),
    "101": Corpus(version="101", description="Alice in Wonderland"),
    "102": Corpus(version="102", description="Call of Cthulhu"),
}
