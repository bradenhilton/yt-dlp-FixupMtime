#!/usr/bin/env python3
import datetime
import os
import shutil
import sys
import tempfile
import unittest


from pathlib import Path


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from yt_dlp_plugins.postprocessor.fixup_mtime import FixupMtimePP


class TestFixupMtimePP(unittest.TestCase):
    def setUp(self):
        self.pp = FixupMtimePP()

        # Create a temporary directory of files, set their initial mtime
        self.temp_dir = tempfile.mkdtemp()
        self.files = [Path(self.temp_dir, filename) for filename in ['test.mp4', 'test.jpg', 'test.info.json', 'test2.mp4']]
        self.initial_mtime = 1234567890.0
        for path in self.files:
            path.touch()
            os.utime(path, (self.initial_mtime, self.initial_mtime))

        self.info = {'filepath': self.files[0], 'upload_date': '20120101'}

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test__striptime_or_none_with_none_timestamp(self):
        timestamp = None
        format_code = self.pp._mtime_format
        expected = None
        self.assertEqual(self.pp._strptime_or_none(timestamp, format_code), expected)

    def test__strptime_or_none_with_invalid_timestamp(self):
        timestamp = 'foobar'
        format_code = self.pp._mtime_format
        expected = None
        self.assertEqual(self.pp._strptime_or_none(timestamp, format_code), expected)

    def test__strptime_or_none_with_valid_timestamp(self):
        timestamp = 1672531200.0
        format_code = self.pp._mtime_format
        expected = datetime.datetime(year=2023, month=1, day=1, tzinfo=datetime.timezone.utc)
        self.assertEqual(self.pp._strptime_or_none(timestamp, format_code), expected)

    def test__strptime_or_none_with_valid_string(self):
        timestamp = '20230101'
        format_code = self.pp._mtime_format
        expected = datetime.datetime(year=2023, month=1, day=1)
        self.assertEqual(self.pp._strptime_or_none(timestamp, format_code), expected)

    def test__strptime_or_none_with_valid_string_and_guess_format(self):
        timestamp = '2023/01/01'
        format_code = self.pp._mtime_format
        expected = datetime.datetime(year=2023, month=1, day=1)
        self.assertEqual(self.pp._strptime_or_none(timestamp, format_code), expected)

    def test__strptime_or_none_with_valid_string_and_valid_format_code(self):
        timestamp = '2023-01-01'
        format_code = '%Y-%m-%d'
        expected = datetime.datetime(year=2023, month=1, day=1)
        self.assertEqual(self.pp._strptime_or_none(timestamp, format_code), expected)

    def test__get_related_files(self):
        filepath = self.info.get('filepath')
        expected = [path for path in self.files if path.name in ['test.mp4', 'test.jpg', 'test.info.json']]
        self.assertCountEqual(self.pp._get_related_files(filepath), expected)

    def test__get_mtime_with_existing_mtime(self):
        filepath = self.info.get('filepath')
        custom_key = 'mtime'
        expected = self.initial_mtime
        self.assertEqual(self.pp._get_mtime(filepath, self.info, custom_key), expected)

    def test__get_mtime_with_custom_key(self):
        filepath = self.info.get('filepath')
        custom_key = 'upload_date'
        expected = self.info.get(custom_key)
        self.assertEqual(self.pp._get_mtime(filepath, self.info, custom_key), expected)

    def test__get_mtime_with_invalid_key(self):
        filepath = self.info.get('filepath')
        custom_key = None
        expected = None
        self.assertEqual(self.pp._get_mtime(filepath, self.info, custom_key), expected)

    def test__set_mtime_of_files(self):
        new_mtime = datetime.datetime(year=2023, month=1, day=1, tzinfo=datetime.timezone.utc)
        self.pp._set_mtime_of_files(self.files, new_mtime)
        for path in self.files:
            self.assertEqual(os.path.getmtime(path), new_mtime.timestamp())

    def test_run(self):
        self.pp._mtime_key = 'upload_date'
        self.pp._mtime_format = '%Y%m%d'
        expected = datetime.datetime(year=2012, month=1, day=1, tzinfo=datetime.timezone.utc).timestamp()
        self.pp.run(self.info)
        for path in self.files[:3]:
            self.assertEqual(os.path.getmtime(path), expected)
        self.assertNotEqual(os.path.getmtime(self.files[3]), expected)


if __name__ == '__main__':
    unittest.main()
