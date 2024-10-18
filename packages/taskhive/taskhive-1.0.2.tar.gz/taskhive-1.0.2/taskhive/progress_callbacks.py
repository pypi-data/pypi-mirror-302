from typing import Callable, Tuple


def finishedProcessingCallback(finishedCallback: Callable[[object], None], dr: Tuple[str, object], progress):
    descriptor, result = dr
    if hasattr(progress, "desc"):
        progress.desc = f'Finished processing {descriptor}'
    if hasattr(progress, "update"):
        progress.update()
    if finishedCallback:
        finishedCallback(result)
