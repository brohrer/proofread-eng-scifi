"""
A second-order Markov Model for predicting the liklihood of a language
token, given the previous token.
"""

import os
import sqlite3
import numpy as np
from proofread_eng_scifi.models.markov_base import MarkovBase


class SecondOrderMarkovModel(MarkovBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.description = "2nd-order Markov"

    def _initialize(self):
        self.transition_counts = np.zeros(
            (self.n_unique_tokens, self.n_unique_tokens, self.n_unique_tokens),
            dtype=np.int32,
        )
        self.transition_probabilities = np.zeros(
            (self.n_unique_tokens, self.n_unique_tokens, self.n_unique_tokens),
            dtype=np.float64,
        )

    def is_ready(self):
        # Check whether the model is trained and loaded
        try:
            if np.sum(self.transition_counts) > 100:
                return True
        except AttributeError:
            pass
        return False

    def _train_from_tokens(self, ids):
        # Doesn't re-initialize. Multiple calls will accumulate
        # training experience.
        for i_transition in range(len(ids) - 2):
            self.transition_counts[
                ids[i_transition], ids[i_transition + 1], ids[i_transition + 2]
            ] += 1

        self.transition_probabilities = (
            self.transition_counts
            / (np.sum(self.transition_counts, axis=2) + self.epsilon)[
                :, :, np.newaxis
            ]
        ) + self.transition_probability_floor

    def _calc_likelihoods(self, ids):
        if len(ids) < 3:
            return None

        # The model doesn't have anything useful to say about the first
        # two tokens, so initialize them by hand.
        likelihoods = [1.0, 1.0]
        for i_transition in range(len(ids) - 2):
            likelihoods.append(
                self.transition_probabilities[
                    ids[i_transition],
                    ids[i_transition + 1],
                    ids[i_transition + 2],
                ]
            )

        return likelihoods


class SparseSecondOrderMarkovModel(MarkovBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.description = "Sparse 2nd-order Markov"

    def _initialize(self):
        self.bigram_counts = {}
        self.trigram_counts = {}

    def is_ready(self):
        # Check whether the model is trained and loaded
        try:
            if (
                len(self.bigram_counts) > self.not_empty_threshold
                and len(self.trigram_counts) > self.not_empty_threshold
            ):
                return True
        except AttributeError:
            pass
        return False

    def _train_from_tokens(self, ids):
        for i_transition in range(len(ids) - 2):
            bigram_key = tuple([ids[i_transition], ids[i_transition + 1]])
            trigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                    ids[i_transition + 2],
                ]
            )
            self.bigram_counts[bigram_key] = (
                self.bigram_counts.get(bigram_key, 0) + 1
            )
            self.trigram_counts[trigram_key] = (
                self.trigram_counts.get(trigram_key, 0) + 1
            )

    def _calc_likelihoods(self, ids):
        if len(ids) < 3:
            return None

        # The model doesn't have anything useful to say about the first
        # two tokens, so initialize them by hand.
        likelihoods = [1.0, 1.0]
        for i_transition in range(len(ids) - 2):
            bigram_key = tuple([ids[i_transition], ids[i_transition + 1]])
            trigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                    ids[i_transition + 2],
                ]
            )
            bigram_count = self.bigram_counts.get(bigram_key, self.epsilon)
            trigram_count = self.trigram_counts.get(trigram_key, 0)
            likelihoods.append(
                trigram_count / bigram_count + self.transition_probability_floor
            )

        return likelihoods


class ConstrainedSparseSecondOrderMarkovModel(MarkovBase):
    def __init__(
        self,
        max_dict_size=int(3e7),
        max_dict_size_after_shrink=int(2e7),
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.model_path = os.path.join(self.model_dir, self.model_filename)
        self.max_dict_size = max_dict_size
        self.max_dict_size_after_shrink = max_dict_size_after_shrink
        self.shrink_count_cutoff = 1
        self.description = "Constrained 2nd-order Markov"

    def _initialize(self):
        self.bigram_counts = {}
        self.trigram_counts = {}

    def is_ready(self):
        # Check whether the model is trained and loaded
        try:
            if (
                len(self.bigram_counts) > self.not_empty_threshold
                and len(self.trigram_counts) > self.not_empty_threshold
            ):
                return True
        except AttributeError:
            pass
        return False

    def _train_from_tokens(self, ids):
        for i_transition in range(len(ids) - 2):
            bigram_key = tuple([ids[i_transition], ids[i_transition + 1]])
            trigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                    ids[i_transition + 2],
                ]
            )
            self.bigram_counts[bigram_key] = (
                self.bigram_counts.get(bigram_key, 0) + 1
            )
            self.trigram_counts[trigram_key] = (
                self.trigram_counts.get(trigram_key, 0) + 1
            )
        self.shrink_model()

    def shrink_model(self):
        print(
            "trigram counts:",
            len(self.trigram_counts),
            "  bigram counts:",
            len(self.bigram_counts),
        )
        if len(self.trigram_counts) > self.max_dict_size:
            while True:
                for trigram_key in list(self.trigram_counts.keys()):
                    count = self.trigram_counts[trigram_key]
                    if count <= self.shrink_count_cutoff:
                        del self.trigram_counts[trigram_key]
                        bigram_key = (trigram_key[0], trigram_key[1])
                        if self.bigram_counts[bigram_key] > count:
                            self.bigram_counts[bigram_key] -= count
                        else:
                            del self.bigram_counts[bigram_key]
                if len(self.trigram_counts) <= self.max_dict_size_after_shrink:
                    break
                else:
                    self.shrink_count_cutoff += 1
                    if self.verbose:
                        print(
                            f"trigram count cutoff increased to {self.shrink_count_cutoff}"
                        )

            print(
                "    after cleanup, ",
                "trigram counts:",
                len(self.trigram_counts),
                "  bigram counts:",
                len(self.bigram_counts),
            )

    def _calc_likelihoods(self, ids):
        if len(ids) < 3:
            return None

        # The model doesn't have anything useful to say about the first
        # two tokens, so initialize them by hand.
        likelihoods = [1.0, 1.0]
        for i_transition in range(len(ids) - 2):
            bigram_key = tuple([ids[i_transition], ids[i_transition + 1]])
            trigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                    ids[i_transition + 2],
                ]
            )
            bigram_count = self.bigram_counts.get(bigram_key, self.epsilon)
            trigram_count = self.trigram_counts.get(trigram_key, 0)
            likelihoods.append(
                trigram_count / bigram_count + self.transition_probability_floor
            )

        return likelihoods


class DBSecondOrderMarkovModel(MarkovBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_dir = os.path.dirname(__file__)
        self.db_name = os.path.join(self.model_dir, f"{self.version}.db")
        self.bigram_table_name = "bigrams"
        self.trigram_table_name = "trigrams"
        self.connection = None
        self.cursor = None
        self.description = "DB 2nd-order Markov"

    def _initialize(self):
        self._connect()
        # Initialize 2 tables, one for bigram counts, one for trigram counts
        self.cursor.execute(f"""
            DROP TABLE IF EXISTS {self.bigram_table_name};
        """)
        self.cursor.execute(f"""
            DROP TABLE IF EXISTS {self.trigram_table_name};
        """)
        self.connection.commit()

        self.cursor.execute(f"""
            CREATE TABLE {self.bigram_table_name}
            (
                tokenid1 INTEGER,
                tokenid2 INTEGER,
                count INTEGER,
                PRIMARY KEY (tokenid1, tokenid2)
            );
        """)
        self.cursor.execute(f"""
            CREATE TABLE {self.trigram_table_name}
            (
                tokenid1 INTEGER,
                tokenid2 INTEGER,
                tokenid3 INTEGER,
                count INTEGER,
                PRIMARY KEY (tokenid1, tokenid2, tokenid3)
            );
        """)

        self.connection.commit()

    def _train_from_tokens(self, ids):
        bigram_keys = []
        trigram_keys = []
        for i_transition in range(len(ids) - 2):
            bigram_keys.append(
                tuple(
                    [
                        ids[i_transition],
                        ids[i_transition + 1],
                    ]
                )
            )
            trigram_keys.append(
                tuple(
                    [
                        ids[i_transition],
                        ids[i_transition + 1],
                        ids[i_transition + 2],
                    ]
                )
            )

        # upsert bigram and trigram counts
        self.cursor.executemany(
            f"""
            INSERT INTO {self.bigram_table_name}
                (tokenid1, tokenid2, count)
                VALUES (?, ?, 1)
            ON CONFLICT(tokenid1, tokenid2) DO
                UPDATE SET count = count + 1;
        """,
            bigram_keys,
        )

        self.cursor.executemany(
            f"""
            INSERT INTO {self.trigram_table_name}
                (tokenid1, tokenid2, tokenid3, count)
                VALUES (?, ?, ?, 1)
            ON CONFLICT(tokenid1, tokenid2, tokenid3) DO
                UPDATE SET count = count + 1;
        """,
            trigram_keys,
        )

        self.connection.commit()

    def _calc_likelihoods(self, ids):
        if len(ids) < 3:
            return None

        self._connect()

        # The model doesn't have anything useful to say about the first
        # two tokens, so initialize them by hand.
        likelihoods = [1.0, 1.0]

        for i_transition in range(len(ids) - 2):
            self.cursor.execute(
                f"""
                SELECT count
                FROM {self.bigram_table_name}
                WHERE tokenid1 = ?
                    AND tokenid2 = ?;
            """,
                (ids[i_transition], ids[i_transition + 1]),
            )
            result = self.cursor.fetchall()
            if len(result) == 0:
                bigram_count = self.epsilon
            else:
                bigram_count = result[0][0]

            self.cursor.execute(
                f"""
                SELECT count
                FROM {self.trigram_table_name}
                WHERE tokenid1 = ?
                    AND tokenid2 = ?
                    AND tokenid3 = ?;
            """,
                (
                    ids[i_transition],
                    ids[i_transition + 1],
                    ids[i_transition + 2],
                ),
            )
            result = self.cursor.fetchall()
            if len(result) == 0:
                trigram_count = 0
            else:
                trigram_count = result[0][0]

            likelihoods.append(
                trigram_count / bigram_count + self.transition_probability_floor
            )

        return likelihoods

    def _save(self):
        pass

    def _load(self):
        self._connect()
        if not self._both_tables_exist():
            # This will trigger a training of the model.
            raise FileNotFoundError

    def _connect(self):
        # https://pytutorial.com/python-sqlite3-pragma-guide-database-configuration/
        if self.connection is None or self.cursor is None:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()

        # Abuse the sqlite db for fast training from a single process.
        memory_size = int(9e9 / 1e3)
        # self.cursor.execute("PRAGMA page_size = 4096")
        self.cursor.execute(f"PRAGMA cache_size = -{memory_size}")  # kb cache
        self.cursor.execute("PRAGMA temp_store = MEMORY")
        # self.cursor.execute(f"PRAGMA mmap_size = {memory_size}")
        self.cursor.execute("PRAGMA journal_mode = OFF")
        self.cursor.execute("PRAGMA synchronous = OFF")

        # Print current settings
        for setting in [
            "page_size",
            "cache_size",
            "temp_store",
            "journal_mode",
            "synchronous",
        ]:
            self.cursor.execute(f"PRAGMA {setting}")
            print(f"{setting}:", self.cursor.fetchone()[0])

    def _both_tables_exist(self):
        # Check whether the model is initialized
        if self.cursor is None:
            return False

        both_tables_exist = True

        self.cursor.execute(f"""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='{self.bigram_table_name}';
        """)
        result = self.cursor.fetchall()
        if len(result) == 0 or result[0][0] == 0:
            both_tables_exist = False

        self.cursor.execute(f"""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='{self.trigram_table_name}';
        """)
        result = self.cursor.fetchall()
        if len(result) == 0 or result[0][0] == 0:
            both_tables_exist = False

        return both_tables_exist

    def is_ready(self):
        if not self._both_tables_exist():
            return False

        ready = True

        self.cursor.execute(f"""
            SELECT COUNT(*) FROM {self.bigram_table_name}
        """)
        if self.cursor.fetchall()[0][0] < self.not_empty_threshold:
            ready = False

        self.cursor.execute(f"""
            SELECT COUNT(*) FROM {self.trigram_table_name}
        """)
        if self.cursor.fetchall()[0][0] < self.not_empty_threshold:
            ready = False

        return ready

    def close(self):
        try:
            self.connection.close()
        except Exception:
            pass


registry = {
    "00": SecondOrderMarkovModel(
        version="00",
        tokenizer_version="04",
        corpus_versions=["00"],
    ),
    "01": SecondOrderMarkovModel(
        version="01",
        tokenizer_version="04",
        corpus_versions=["00", "01"],
    ),
    "02": SparseSecondOrderMarkovModel(
        version="02",
        tokenizer_version="00",
        corpus_versions=["00", "01"],
    ),
    "03": SparseSecondOrderMarkovModel(
        version="03",
        tokenizer_version="05",
        corpus_versions=["02"],
    ),
    "04": SparseSecondOrderMarkovModel(
        version="04",
        tokenizer_version="06",
        corpus_versions=["02"],
    ),
    "05": SparseSecondOrderMarkovModel(
        version="05",
        tokenizer_version="07",
        corpus_versions=["02"],
    ),
    "06": SparseSecondOrderMarkovModel(
        version="06",
        tokenizer_version="08",
        corpus_versions=["02"],
    ),
    "07": SparseSecondOrderMarkovModel(
        version="07",
        tokenizer_version="06",
        corpus_versions=["02"],
    ),
    "08": SparseSecondOrderMarkovModel(
        version="08",
        tokenizer_version="05",
        corpus_versions=["03"],
    ),
    # "09": SparseSecondOrderMarkovModel(
    #     version="09",
    #     tokenizer_version="05",
    #     corpus_versions=["04"],
    # ),
    "10": SparseSecondOrderMarkovModel(
        version="10",
        tokenizer_version="09",
        corpus_versions=["05"],
    ),
    # "11": SparseSecondOrderMarkovModel(
    #     version="11",
    #     tokenizer_version="08",
    #     corpus_versions=["05"],
    # ),
    # "12": SparseSecondOrderMarkovModel(
    #     version="12",
    #     tokenizer_version="07",
    #     corpus_versions=["05"],
    # ),
    # "13": DBSecondOrderMarkovModel(
    #     version="13",
    #     tokenizer_version="05",
    #     corpus_versions=["04"],
    # ),
    # "14": DBSecondOrderMarkovModel(
    #     version="14",
    #     tokenizer_version="07",
    #     corpus_versions=["05"],
    # ),
    # "15": DBSecondOrderMarkovModel(
    #     version="15",
    #     tokenizer_version="05",
    #     corpus_versions=["00"],
    # ),
    "16": ConstrainedSparseSecondOrderMarkovModel(
        version="16",
        tokenizer_version="05",
        corpus_versions=["00"],
    ),
    "17": ConstrainedSparseSecondOrderMarkovModel(
        version="17",
        tokenizer_version="05",
        corpus_versions=["03"],
    ),
    "18": ConstrainedSparseSecondOrderMarkovModel(
        version="18",
        tokenizer_version="05",
        corpus_versions=["04"],
    ),
    "19": ConstrainedSparseSecondOrderMarkovModel(
        version="19",
        tokenizer_version="05",
        corpus_versions=["05"],
    ),
    "20": ConstrainedSparseSecondOrderMarkovModel(
        version="20",
        tokenizer_version="05",
        corpus_versions=["04"],
        max_dict_size=int(4e7),
        max_dict_size_after_shrink=int(3e7),
    ),
    "21": ConstrainedSparseSecondOrderMarkovModel(
        version="21",
        tokenizer_version="05",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
    "22": ConstrainedSparseSecondOrderMarkovModel(
        version="22",
        tokenizer_version="05",
        corpus_versions=["04"],
        max_dict_size=int(6e7),
        max_dict_size_after_shrink=int(5e7),
    ),
    "23": ConstrainedSparseSecondOrderMarkovModel(
        version="23",
        tokenizer_version="05",
        corpus_versions=["04"],
        max_dict_size=int(7e7),
        max_dict_size_after_shrink=int(6e7),
    ),
    # "24": ConstrainedSparseSecondOrderMarkovModel(
    #     version="24",
    #     tokenizer_version="05",
    #     corpus_versions=["04"],
    #     max_dict_size=int(8e7),
    #     max_dict_size_after_shrink=int(7e7),
    # ),
    # "25": ConstrainedSparseSecondOrderMarkovModel(
    #     version="25",
    #     tokenizer_version="05",
    #     corpus_versions=["04"],
    #     max_dict_size=int(9e7),
    #    max_dict_size_after_shrink=int(8e7),
    # ),
    "26": ConstrainedSparseSecondOrderMarkovModel(
        version="26",
        tokenizer_version="06",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
    "27": ConstrainedSparseSecondOrderMarkovModel(
        version="27",
        tokenizer_version="07",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
    "28": ConstrainedSparseSecondOrderMarkovModel(
        version="28",
        tokenizer_version="08",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
    "29": ConstrainedSparseSecondOrderMarkovModel(
        version="29",
        tokenizer_version="09",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
    "30": ConstrainedSparseSecondOrderMarkovModel(
        version="30",
        tokenizer_version="11",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
    "31": ConstrainedSparseSecondOrderMarkovModel(
        version="31",
        tokenizer_version="12",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
    "32": ConstrainedSparseSecondOrderMarkovModel(
        version="32",
        tokenizer_version="13",
        corpus_versions=["04"],
        max_dict_size=int(5e7),
        max_dict_size_after_shrink=int(4e7),
    ),
}
