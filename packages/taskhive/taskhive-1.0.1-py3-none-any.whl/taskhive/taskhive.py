from collections.abc import Sized
from tqdm import tqdm
from yaspin import yaspin
from multiprocessing import Manager, Pool
from typing import List, Callable, TypeVar, Generic, Tuple, Optional, Iterable, Union
from .progress_callbacks import finishedProcessingCallback
from .workers import getWorkerId, releaseWorkerId

W = TypeVar('W')
R = TypeVar('R')


class TaskHive(Generic[W, R]):
    def __init__(
        self,
        numWorkers: int,
        works: Union[List[W], Iterable[W]],
    ):
        self.numWorkers = numWorkers
        self.works = works

    def workProcessingCallback(self, lock, availableWorkers, processingCallback: Callable[[int, W],
                               Tuple[str, R]], work: W) -> Tuple[str, R]:
        workerId = getWorkerId(lock, availableWorkers)
        result = processingCallback(workerId, work)
        releaseWorkerId(lock, availableWorkers, workerId)
        return result

    def errorProcessingCallback(self, errorCallback: Optional[Callable[[BaseException], None]], e: BaseException) -> None:
        if errorCallback:
            errorCallback(e)
        else:
            print(f"Error: {e}")
        exit(1)

    def processWork(
        self,
        processingCallback: Callable[[int, W], Tuple[str, R]],
        finishedCallback: Callable[[R], None],
        errorCallback: Optional[Callable[[BaseException], None]] = None,
        desc: str = "Processing ...",
        *args,
        **kwargs
    ) -> None:
        with Manager() as manager:
            lock = manager.Lock()
            availableWorkerIds = manager.list(range(self.numWorkers, 0, -1))

            if isinstance(self.works, Sized):
                total = len(self.works)
                with tqdm(total=total, desc=desc, position=0, *args, **kwargs) as pbar:
                    self._run_with_progress_bar(lock, processingCallback, finishedCallback, errorCallback, pbar)
            else:
                with yaspin(text=desc) as spinner:
                    self._run_with_spinner(lock, processingCallback, finishedCallback, errorCallback, spinner)

    def _run_with_progress_bar(self, lock, processingCallback, finishedCallback, errorCallback, pbar):
        if self.numWorkers == 1:
            try:
                for work in self.works:
                    result = self.workProcessingCallback(lock, availableWorkerIds, processingCallback, work)
                    finishedProcessingCallback(finishedCallback, result, pbar)
            except Exception as e:
                self.errorProcessingCallback(errorCallback, e)
        else:
            with Pool(processes=self.numWorkers) as pool:
                for work in self.works:
                    pool.apply_async(
                        self.workProcessingCallback,
                        args=(lock, availableWorkerIds, processingCallback, work),
                        callback=lambda res: finishedProcessingCallback(finishedCallback, res, pbar),
                        error_callback=lambda e: self.errorProcessingCallback(errorCallback, e),
                    )
                pool.close()
                pool.join()

    def _run_with_spinner(self, lock, processingCallback, finishedCallback, errorCallback, spinner):
        if self.numWorkers == 1:
            try:
                for work in self.works:
                    result = self.workProcessingCallback(lock, availableWorkerIds, processingCallback, work)
                    finishedProcessingCallback(finishedCallback, result, spinner)
            except Exception as e:
                self.errorProcessingCallback(errorCallback, e)
        else:
            with Pool(processes=self.numWorkers) as pool:
                for work in self.works:
                    pool.apply_async(
                        self.workProcessingCallback,
                        args=(lock, availableWorkerIds, processingCallback, work),
                        callback=lambda res: finishedProcessingCallback(finishedCallback, res, spinner),
                        error_callback=lambda e: self.errorProcessingCallback(errorCallback, e),
                    )
                pool.close()
                pool.join()
