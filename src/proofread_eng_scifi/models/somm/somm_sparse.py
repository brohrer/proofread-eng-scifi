from proofread_eng_scifi.models.somm.somm import SecondOrderMarkovModel


class SparseSecondOrderMarkovModel(SecondOrderMarkovModel):
    def initialize(self):
        self.bigram_counts = {}
        self.trigram_counts = {}

    def train_from_tokens(self, ids):
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

    def calculate_likelihoods(self, ids):
        if len(ids) < 3:
            return None

        likelihoods = []
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
