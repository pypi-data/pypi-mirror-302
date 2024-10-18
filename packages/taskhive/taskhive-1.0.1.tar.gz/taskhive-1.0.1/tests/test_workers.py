from taskhive.workers import getWorkerId, releaseWorkerId
from multiprocessing import Manager
import pytest


@pytest.fixture
def manager():
    return Manager()


def test_get_and_release_worker_id(manager):
    lock = manager.Lock()
    availableWorkers = manager.list([1, 2, 3])

    worker_id = getWorkerId(lock, availableWorkers)
    assert worker_id == 3
    assert len(availableWorkers) == 2

    releaseWorkerId(lock, availableWorkers, worker_id)
    assert len(availableWorkers) == 3
