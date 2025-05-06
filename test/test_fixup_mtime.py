#!/usr/bin/env python3
import os
import shutil
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from yt_dlp_plugins.postprocessor.fixup_mtime import FixupMtimePP


class TestFixupMtimePP(unittest.TestCase):
    def setUp(self):
        self.pp = FixupMtimePP()
        self.root_dir = Path(__file__).resolve().parent.parent
        self.test_files_dir = self.root_dir.joinpath("test_files")

        # Create a temporary directory of files, set their initial mtime
        file_path = self.test_files_dir.joinpath("test äةُ한汉漢なナอัй.mp4").relative_to(self.root_dir)
        self.info = {"filepath": str(file_path), "upload_date": "20120101"}
        self.files = [
            file_path,
            file_path.with_suffix(""),
            file_path.with_suffix(".jpg"),
            file_path.with_suffix(".info.json"),
            self.test_files_dir.joinpath("test2.mp4"),
        ]
        self.initial_mtime = 1234567890.0
        self.test_files_dir.mkdir(parents=True, exist_ok=True)
        for path in self.files:
            path.touch()
            os.utime(path, (self.initial_mtime, self.initial_mtime))

    def tearDown(self):
        shutil.rmtree(self.test_files_dir)

    def test__strptime_or_none_with_none_timestamp(self):
        timestamp = None
        format_code = self.pp._mtime_format
        expected = None
        assert self.pp._strptime_or_none(timestamp, format_code) == expected

    def test__strptime_or_none_with_invalid_timestamp(self):
        timestamp = "foobar"
        format_code = self.pp._mtime_format
        expected = None
        assert self.pp._strptime_or_none(timestamp, format_code) == expected

    def test__strptime_or_none_with_valid_timestamp(self):
        timestamp = 1672531200.0
        format_code = self.pp._mtime_format
        expected = datetime(year=2023, month=1, day=1, tzinfo=timezone.utc)
        assert self.pp._strptime_or_none(timestamp, format_code) == expected

    def test__strptime_or_none_with_valid_string(self):
        timestamp = "20230101"
        format_code = self.pp._mtime_format
        expected = datetime(year=2023, month=1, day=1)  # noqa: DTZ001
        assert self.pp._strptime_or_none(timestamp, format_code) == expected

    def test__strptime_or_none_with_valid_string_and_guess_format(self):
        timestamp = "2023/01/01"
        format_code = self.pp._mtime_format
        expected = datetime(year=2023, month=1, day=1)  # noqa: DTZ001
        assert self.pp._strptime_or_none(timestamp, format_code) == expected

    def test__strptime_or_none_with_valid_string_and_valid_format_code(self):
        timestamp = "2023-01-01"
        format_code = "%Y-%m-%d"
        expected = datetime(year=2023, month=1, day=1)  # noqa: DTZ001
        assert self.pp._strptime_or_none(timestamp, format_code) == expected

    def test__get_related_files(self):
        filepath = self.info.get("filepath")
        expected = list(filter(lambda fpath: not fpath.name.startswith("test2"), self.files))
        self.assertCountEqual(self.pp._get_related_files(filepath), expected)  # noqa: PT009

    def test__get_mtime_with_existing_mtime(self):
        filepath = self.info.get("filepath")
        custom_key = "mtime"
        expected = self.initial_mtime
        assert self.pp._get_mtime(filepath, self.info, custom_key) == expected

    def test__get_mtime_with_custom_key(self):
        filepath = self.info.get("filepath")
        custom_key = "upload_date"
        expected = self.info.get(custom_key)
        assert self.pp._get_mtime(filepath, self.info, custom_key) == expected

    def test__get_mtime_with_invalid_key(self):
        filepath = self.info.get("filepath")
        custom_key = None
        expected = None
        assert self.pp._get_mtime(filepath, self.info, custom_key) == expected

    def test__set_mtime_of_files(self):
        new_mtime = datetime(year=2023, month=1, day=1, tzinfo=timezone.utc)
        self.pp._set_mtime_of_files(self.files, new_mtime)
        for path in self.files:
            assert os.path.getmtime(path) == new_mtime.timestamp()

    def test_run(self):
        self.pp._mtime_key = "upload_date"
        self.pp._mtime_format = "%Y%m%d"
        expected = datetime(year=2012, month=1, day=1, tzinfo=timezone.utc).timestamp()
        self.pp.run(self.info)
        for file in list(filter(lambda fpath: not fpath.name.startswith("test2"), self.files)):
            assert file.stat().st_mtime == expected
        for file in list(filter(lambda fpath: fpath.name.startswith("test2"), self.files)):
            assert file.stat().st_mtime != expected

    def test_run_with_invalid_mtime_key(self):
        self.pp._mtime_key = "invalid"
        with patch.object(self.pp, "to_screen") as mock_to_screen:
            self.pp.run(self.info)
            mock_to_screen.assert_called_with(f"Unable to set mtime to `{self.pp._mtime_key}`")


if __name__ == "__main__":
    unittest.main()
