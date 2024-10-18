from taskhive.workers import getWorkerId, releaseWorkerId
from multiprocessing import Manager
import pytest


@pytest.fixture
def manager():
    manager = Manager()
    try:
        yield manager
    finally:
        manager.shutdown()  # Ensure Manager is closed after test completion


def test_get_and_release_worker_id(manager):
    # Setup: create a lock and availableWorkers list using Manager
    lock = manager.Lock()
    availableWorkers = manager.list([1, 2, 3])

    # Get a worker ID from the pool
    worker_id = getWorkerId(lock, availableWorkers)
    assert worker_id == 3, "The last worker (3) should have been assigned first."
    assert len(availableWorkers) == 2, "There should be two workers left after assigning one."

    # Release the worker back to the pool
    releaseWorkerId(lock, availableWorkers, worker_id)
    assert len(availableWorkers) == 3, "The pool should have three workers after releasing one."
    assert availableWorkers[-1] == 3, "The released worker (3) should be the last in the pool."

