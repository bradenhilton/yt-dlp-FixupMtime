# yt-dlp-FixupMtime

A [yt-dlp](https://github.com/yt-dlp/yt-dlp) postprocessor [plugin](https://github.com/yt-dlp/yt-dlp#plugins) which sets the mtime of all files to a given datetime value by key.

This postprocessor does not support all possible files output by yt-dlp, namely `*.dump` files.

NOTE: This postprocessor should not be run before files are downloaded.

## Installation

Requires yt-dlp `2023.01.02` or above.

You can install this package with pip:

```console
python3 -m pip install -U https://github.com/bradenhilton/yt-dlp-FixupMtime/archive/master.zip
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## Usage

```text
--use-postprocessor FixupMtime[:;[mtime_key=<key>][mtime_format=<format>]]
```

Where `<key>` is the key of your desired datetime within the infojson dictionary and `<format>` is the format of the datetime.

The default value for `mtime_key` is `mtime`, which will set the mtime of all files (thumbnails, subtitles etc.) to the existing mtime of the video. If `mtime_key` is `mtime` and `--mtime` was passed to yt-dlp at the time of download, the value will be the datetime of the last-modified header.

The default value for `mtime_format` is `%Y%m%d`. The postprocessor will also attempt to guess the format with yt-dlp's internal list of formats.

## Examples

Set the mtime of all files to the existing mtime of the video:

```text
--use-postprocessor FixupMtime
```

Set the mtime of all files to the upload date of the video:

```text
--use-postprocessor FixupMtime:mtime_key=upload_date
```

Set the mtime of all files using a custom datetime and format:

```text
--use-postprocessor FixupMtime:mtime_key=meta_date;mtime_format=%Y-%m-%dT%H.%M.%S
```
