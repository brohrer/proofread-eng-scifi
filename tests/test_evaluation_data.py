from data.eval.spelling import evaluation_dataset


def test_data_loading():
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
                wrong_text_index = paragraph.index(' ' + wrong_text + ' ') + 1
            except ValueError:
                wrong_text_index = paragraph.index(wrong_text)

            print(
                f'wrong text starts at {wrong_text_index},' +
                f' with length of {len(wrong_text)}'
            )
            assert wrong_text == extracted_text
