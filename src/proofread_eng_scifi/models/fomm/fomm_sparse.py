from proofread_eng_scifi.models.fomm.fomm import FirstOrderMarkovModel


class SparseFirstOrderMarkovModel(FirstOrderMarkovModel):
    def initialize(self):
        self.unigram_counts = {}
        self.bigram_counts = {}

    def train_from_tokens(self, ids):
        for i_transition in range(len(ids) - 1):
            unigram_key = tuple([ids[i_transition]])
            bigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                ]
            )
            self.unigram_counts[unigram_key] = (
                self.unigram_counts.get(unigram_key, 0) + 1
            )
            self.bigram_counts[bigram_key] = (
                self.bigram_counts.get(bigram_key, 0) + 1
            )

    def calculate_likelihoods(self, ids):
        if len(ids) < 2:
            return None

        likelihoods = []
        for i_transition in range(len(ids) - 1):
            unigram_key = tuple([ids[i_transition]])
            bigram_key = tuple(
                [
                    ids[i_transition],
                    ids[i_transition + 1],
                ]
            )
            unigram_count = self.unigram_counts.get(unigram_key, self.epsilon)
            bigram_count = self.bigram_counts.get(bigram_key, 0)
            likelihoods.append(
                bigram_count / unigram_count + self.transition_probability_floor
            )

        return likelihoods
