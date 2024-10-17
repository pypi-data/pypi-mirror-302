import time, aiohttp, asyncio
from ..functions import Hkeys
from ..scripts import Scripted
from ..functions import Config
from ..functions import SMessage
from ..functions import Cancelled
#====================================================================================

class Aioxdl:

    def __init__(self, **kwargs):
        self.dsizes = 0
        self.tsizes = 0
        self.chunks = 1024
        self.kwords = Config.DATA01
        self.kwords.update(kwargs)

#====================================================================================

    async def start(self, url, location, progress, progress_args):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **self.kwords) as response:
                self.tsizes += await self.getsizes(response)
                with open(location, "wb") as handlexo:
                    while True:
                        chunks = await response.content.read(self.chunks)
                        if not chunks:
                            break
                        handlexo.write(chunks)
                        self.dsizes += self.chunks
                        try: await self.display(progress, progress_args)
                        except ZeroDivisionError: pass

                await response.release()
                return location if location else None
    
#====================================================================================

    async def getsizes(self, response):
        return int(response.headers.get("Content-Length", 1))

#====================================================================================

    async def display(self, progress, progress_args):
        if progress:
            await progress(self.tsizes, self.dsizes, *progress_args)

#====================================================================================

    async def download(self, url, location, progress=None, progress_args=()):
        try:
            location = await self.start(url, location, progress, progress_args)
            return SMessage(result=location, status=200)
        except aiohttp.ClientConnectorError as errors:
            return SMessage(errors=errors, status=400)
        except asyncio.TimeoutError:
            errors = Scripted.DATA01
            return SMessage(errors=errors, status=400)
        except Cancelled as errors:
            return SMessage(errors=errors, status=300)
        except Exception as errors:
            return SMessage(errors=errors, status=400)

#====================================================================================
