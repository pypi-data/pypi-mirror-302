

def getWorkerId(lock, availableWorkers):
    worker_id = None
    while worker_id is None:
        with lock:
            if availableWorkers:
                worker_id = availableWorkers.pop()
    return worker_id


def releaseWorkerId(lock, availableWorkers, worker_id):
    with lock:
        availableWorkers.append(worker_id)
