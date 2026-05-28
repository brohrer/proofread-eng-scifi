from capitalization import evaluation_dataset as capitalization_dataset
from spelling import evaluation_dataset as spelling_dataset

evaluation_datasets = [
    capitalization_dataset,
    spelling_dataset,
]


def test_data_loading():
    for evaluation_dataset in evaluation_datasets:
        assert len(evaluation_dataset) == 5

        for corpus in evaluation_dataset:
            paragraph = " ".join(corpus["paragraph"].split("\n")).strip()
            print(paragraph)
            assert len(corpus["mistakes"]) == 10

            for mistake in corpus["mistakes"]:
                wrong_text = mistake["wrong_text"]
                correct_text = mistake["correct_text"]
                first = mistake["first_char"]
                last = mistake["last_char"]

                print(f'currently "{wrong_text}"')
                print(f'should be "{correct_text}"')
                extracted_text = paragraph[first : last + 1]
                print(f'check wrong text: "{extracted_text}"')

                try:
                    wrong_text_index = paragraph.index(" " + wrong_text + " ") + 1
                except ValueError:
                    wrong_text_index = paragraph.index(wrong_text)

                print(
                    f"wrong text first character {wrong_text_index},"
                    + f" last character {wrong_text_index + len(wrong_text) - 1}"
                )
                assert wrong_text == extracted_text
