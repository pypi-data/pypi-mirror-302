import asyncio
from collections.abc import Callable
from .Uncompress import Uncompress


class Unzip(Uncompress):
    """
    Unzip the file.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        super(Unzip, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
