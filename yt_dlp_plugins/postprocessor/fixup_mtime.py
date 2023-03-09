import contextlib
import datetime
import os
import re


from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import date_formats, replace_extension


class FixupMtimePP(PostProcessor):
    def __init__(self, downloader=None, mtime_key='mtime', format='%Y%m%d'):
        super().__init__(downloader)
        self._mtime_key = mtime_key
        self._format = re.sub(r'%%', '%', format)

    def _strptime_or_none(self, timestamp, format, default=None):
        datetime_object = None
        try:
            if isinstance(timestamp, (int, float)):
                datetime_object = datetime.datetime.fromtimestamp(
                    timestamp, datetime.timezone.utc)
            elif isinstance(timestamp, str):
                formats = [format]
                formats.extend(date_formats(day_first=True))
                for expression in formats:
                    with contextlib.suppress(ValueError):
                        datetime_object = datetime.datetime.strptime(
                            timestamp, expression)
            return datetime_object
        except (ValueError, TypeError, AttributeError):
            return default

    def run(self, info):
        filepath = info.get('filepath')
        if filepath:
            files = {filepath, info.get('__infojson_filename')}
            for path in info.get('__files_to_move'):
                files.add(path)
            if self.get_param('writedescription', False):
                files.add(replace_extension(filepath, 'description'))
            mtime = self._strptime_or_none(os.stat(
                filepath).st_mtime if self._mtime_key == 'mtime'else info.get(self._mtime_key), self._format)
            if mtime:
                self.to_screen(
                    f'Setting mtime of files to {mtime.isoformat()}')
                for file in files:
                    self.try_utime(file, mtime.timestamp(), mtime.timestamp())
            else:
                self.to_screen('Unable to set mtime')
        return [], info
