import datetime
import os
from yt_dlp.postprocessor.common import PostProcessor
from yt_dlp.utils import traverse_obj, datetime_from_str, replace_extension


class FixupMtimePP(PostProcessor):
    def __init__(self, downloader=None, mtime_key=None):
        super().__init__(downloader)
        self._mtime_key = mtime_key

    def run(self, info):
        filepath = info.get('filepath')

        if filepath:
            files = {
                filepath,
                info.get('__infojson_filename'),
            }

            if self.get_param('keepvideo', False):
                for format in traverse_obj(info, ('requested_formats', ...)) or []:
                    format_id = format.get('format_id')
                    format_ext = format.get('ext')

                    if format_id and format_ext:
                        files.add(replace_extension(
                            filepath, f'f{format_id}.{format_ext}'))

            for path in info.get('__files_to_move'):
                files.add(path)

            if self.get_param('writedescription', False):
                files.add(replace_extension(filepath, 'description'))

            mtime = datetime.datetime.fromtimestamp(os.stat(
                filepath).st_mtime, datetime.timezone.utc) if self._mtime_key == 'mtime' else datetime_from_str(info.get(self._mtime_key))

            if mtime:
                self.to_screen(
                    f'Setting mtime of files to {mtime.isoformat()}')
                for file in files:
                    self.try_utime(file, mtime.timestamp(), mtime.timestamp())
        return [], info
