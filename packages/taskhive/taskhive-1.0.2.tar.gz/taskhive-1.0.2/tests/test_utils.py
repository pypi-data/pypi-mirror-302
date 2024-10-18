from taskhive.utils import processSingleData


def test_process_single_data():
    input_data = 5
    result = processSingleData(input_data)
    assert result == input_data * 2
