<p align="center">
    📦 <a href="https://pypi.org/project/aioxdl" style="text-decoration:none;">AIO DOWNLOADER</a>
</p>

<p align="center">
   <a href="https://telegram.me/clinton_abraham"><img src="https://img.shields.io/badge/𝑪𝒍𝒊𝒏𝒕𝒐𝒏 𝑨𝒃𝒓𝒂𝒉𝒂𝒎-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/Space_x_bots"><img src="https://img.shields.io/badge/Sᴘᴀᴄᴇ ✗ ʙᴏᴛꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/sources_codes"><img src="https://img.shields.io/badge/Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
</p>

## INSTALLATION
```bash
pip install aioxdl
```

## USAGE

```python
import time
import asyncio
from aioxdl.modules import Aioxdl
from aioxdl.modules import Filename

async def progress(tsize, dsize, stime):
    # stime = start_time
    # tsize = total_size
    # dsize = download_size
    percentage = round((dsize / tsize) * 100, 2)
    print("\rCOMPLETED : {}%".format(percentage), end="", flush=True)

async def main():
    core = Aioxdl(timeout=2000)
    link = "https://example.link/file.txt"
    loca = await Filename.filename(link)
    file = await core.download(link, loca.result, progress=progress, progress_args=(time.time()))
    fine = file.result if file.errors == None else file.errors
    print(fine)

asyncio.run(main())
```

## GET FILENAME
```python
from aioxdl.modules import Filename

async def main():
    link = "https://example.link/file.txt"
    name = await Filename.get(link)
    print(name.result)

asyncio.run(main())
```


## STOP DOWNLOAD
```python
import time
import asyncio
from aioxdl.modules import Aioxdl
from aioxdl.modules import Filename
from aioxdl.functions import Cancelled

TASK_ID = []

async def progress(tsize, dsize, stime, tuid):
    # stime = start_time
    # tsize = total_size
    # dsize = download_size
    if tuid in TASK_ID:
        percentage = round((dsize / tsize) * 100, 2)
        print("\rCOMPLETED : {}%".format(percentage), end="", flush=True)
    else:
        raise Cancelled("Cancelled ❌")

async def main():
    tims = time.time()
    tuid = 1234567890
    TASK_ID.append(tuid)
    core = Aioxdl(timeout=2000)
    link = "https://example.uri/file.txt"
    loca = await Filename.filename(link)
    file = await core.download(link, loca.result,
                               progress=progress, progress_args=(tims, tuid))
    if file.status == 400:
        print(file.errors)
    elif file.status == 300:
        print("Cancelled ❌")
    else:
        print(fine.result)

asyncio.run(main())
```
