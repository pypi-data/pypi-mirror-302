import pytest
from multiprocessing import Manager
from taskhive.taskhive import TaskHive
from taskhive.utils import processSingleData


def mock_innerProcessData(workerId, data):
    descriptor = f"{data} from worker {workerId}"
    result = processSingleData(data)
    return descriptor, result


@pytest.fixture
def manager():
    return Manager()


def test_taskhive_single_worker(manager):
    works = [1, 2, 3]
    numWorkers = 1
    resultList = []

    def finishedProcessingCallback(result):
        resultList.append(result)

    def errorCallback(error):
        pytest.fail(f"Unexpected error: {error}")

    executor = TaskHive(numWorkers, works)
    executor.processWork(mock_innerProcessData, finishedProcessingCallback, errorCallback, desc="Running Test")

    assert len(resultList) == len(works)


def test_taskhive_multiple_workers(manager):
    works = [1, 2, 3]
    numWorkers = 2
    resultList = []

    def finishedProcessingCallback(result):
        resultList.append(result)

    def errorCallback(error):
        pytest.fail(f"Unexpected error: {error}")

    executor = TaskHive(numWorkers, works)
    executor.processWork(mock_innerProcessData, finishedProcessingCallback, errorCallback, desc="Running Test")

    assert len(resultList) == len(works)
