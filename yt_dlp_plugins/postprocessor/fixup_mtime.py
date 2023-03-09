import contextlib
import datetime
import glob
import os
import re


from pathlib import Path
from typing import Iterable, List, Optional, Union


from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import date_formats


class FixupMtimePP(PostProcessor):
    def __init__(self, downloader=None, mtime_key: str = 'mtime', mtime_format: str = '%Y%m%d') -> None:
        super().__init__(downloader)
        self._mtime_key = mtime_key
        self._mtime_format = re.sub(r'%%', '%', mtime_format)

    def _strptime_or_none(self, timestamp: Union[float, int, str], format_code: str) -> Optional[datetime.datetime]:
        if isinstance(timestamp, (float, int)):
            return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
        for code in [format_code] + date_formats(day_first=True):
            with contextlib.suppress(ValueError):
                return datetime.datetime.strptime(timestamp, code)
        return None

    def _get_related_files(self, filepath: Union[Path, str]) -> List[Path]:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        return [Path(path) for path in filepath.parent.glob(f'{glob.escape(filepath.stem)}.*')
                if path.is_file()]

    def _get_mtime(self, filepath: Path, info: dict, mtime_key: str) -> Optional[Union[float, int, str]]:
        return os.path.getmtime(filepath) if mtime_key == 'mtime' else info.get(mtime_key)

    def _set_mtime_of_files(self, files: Iterable[Path], mtime: Union[datetime.datetime, float, int]) -> None:
        if isinstance(mtime, datetime.datetime):
            mtime = mtime.timestamp()
        for path in files:
            self.try_utime(str(path), os.path.getatime(path), mtime)

    def run(self, info: dict):
        filepath = info.get('filepath')
        if filepath:
            mtime = self._strptime_or_none(self._get_mtime(
                filepath, info, self._mtime_key), self._mtime_format)
            if mtime:
                self.to_screen(
                    f'Setting mtime of files to `{self._mtime_key}` ({mtime.isoformat()})')
                self._set_mtime_of_files(self._get_related_files(filepath), mtime)
            else:
                self.to_screen(f'Unable to set mtime to `{self._mtime_key}`')
        return [], info
