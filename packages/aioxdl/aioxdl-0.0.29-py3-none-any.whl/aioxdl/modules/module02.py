from ..functions import Hkeys
from ..scripts import Scripted
from ..functions import SMessage
from yt_dlp import YoutubeDL, DownloadError
#===================================================================================

class Filename:

    async def get(filelink):
        with YoutubeDL(Hkeys.DATA01) as ydl:
            try:
                response = ydl.extract_info(filelink, download=False)
                filename = ydl.prepare_filename(response, outtmpl=Hkeys.DATA02)
                return SMessage(result=filename)
            except DownloadError as errors:
                return SMessage(result=Scripted.DATA02, errors=errors)
            except Exception as errors:
                return SMessage(result=Scripted.DATA02, errors=errors)

#===================================================================================
