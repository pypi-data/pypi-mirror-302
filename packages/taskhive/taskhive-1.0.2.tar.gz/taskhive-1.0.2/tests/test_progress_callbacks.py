from taskhive.progress_callbacks import finishedProcessingCallback


def mock_finished_callback(result):
    assert result == 10


def test_finished_processing_callback():
    descriptor = "Test Descriptor"
    result = 10

    # Modify 'update' to accept a positional argument
    mock_progress = type('MockProgress', (object,), {'desc': None, 'update': lambda n: None})()

    finishedProcessingCallback(mock_finished_callback, (descriptor, result), mock_progress)
    assert mock_progress.desc == f"Finished processing {descriptor}"

