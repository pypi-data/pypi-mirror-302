import asyncio
from collections.abc import Callable
from navconfig.logging import logging
from ..exceptions import FileNotFound, ComponentError, FileError
from .DownloadFrom import DownloadFromBase
from .Sharepoint import Sharepoint


class DownloadFromSharepoint(Sharepoint, DownloadFromBase):
    """
    DownloadFromSharepoint

    Overview

            This Sharepoint component downloads a file or uploads it to the Microsoft Sharepoint
            service

        .. table:: Properties
        :widths: auto


    +--------------+----------+-----------+-------------------------------------------------------+
    | Name         | Required | Summary                                                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    | credentials  |   Yes    | Credentials to establish connection with sharepoint if it is null |
    |              |          | get the credentials of the environment                            |
    +--------------+----------+-----------+-------------------------------------------------------+
    | file_id      |   Yes    | Identificador del archivo en sharepoint                           |
    +--------------+----------+-----------+-------------------------------------------------------+
    | destination  |   Yes    | Format of how I will save the file                                |
    +--------------+----------+-----------+-------------------------------------------------------+

    Return the list of arbitrary days

    """
    """
    DownloadFromSharepoint.

    **Overview**

        This Sharepoint component downloads a file or uploads it to the Microsoft Sharepoint service

    **Properties** (inherited from DownloadFromBase and Sharepoint)

    .. table:: Properties
        :widths: auto

        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | Name               | Required | Summary                                                                          |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | credentials        |   Yes    | Credentials to establish connection with SharePoint site (username and password) |
        |                    |          | get credentials from environment if null.                                        |  
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | site               |   Yes    | The URL of the SharePoint site.                                                  |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | verify             |   No     | Whether to verify the SSL certificate of the SharePoint site (default: True).    |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | timeout            |   No     | The timeout value for SharePoint operations (default: 30 seconds).               |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | create_destination |   No     | Boolean flag indicating whether to create the destination directory if it        |
        |                    |          | doesn't exist (default: True).                                                   |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | tenant             |   Yes    | Is the set of site collections of SharePoint                                     |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
        | file_id            |   Yes    | Identificador del archivo en sharepoint                                          |
        +--------------------+----------+-----------+----------------------------------------------------------------------+
    
    Save the downloaded files on the new destination.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.url: str = None
        self.folder = None
        self.rename: str = None
        self.context = None
        DownloadFromBase.__init__(
            self, loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        params = self._params.copy()
        Sharepoint.__init__(self, **params)

    def start(self):
        super(DownloadFromSharepoint, self).start()
        # print(self.context)
        return True

    async def close(self):
        pass

    async def run(self):
        await self.connection()
        if self.context:
            try:
                if hasattr(self, 'file') and "pattern" in self.file:  # search-like context
                    filenames = await self.file_search()
                else:
                    filenames = await self.file_download()
                self._result = filenames
                self.add_metric("SHAREPOINT_FILES", self._result)
                return self._result
            except (FileError, FileNotFound):
                raise
            except Exception as err:
                logging.error(f"Error downloading File: {err}")
                raise FileError(
                    f"Error downloading File: {err}"
                ) from err
        else:
            raise ComponentError("Sharepoint: Error connecting to Resource Context.")
