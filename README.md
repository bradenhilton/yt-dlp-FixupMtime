# yt-dlp-FixupMtime

A [yt-dlp](https://github.com/yt-dlp/yt-dlp) postprocessor [plugin](https://github.com/yt-dlp/yt-dlp#plugins) that sets the mtime of all files to a given datetime value by key.

Some file types (namely `*.dump` files) that can be optionally output by yt-dlp when downloading are not supported.

NOTE: This postprocessor should not be run before files are downloaded. The default `when` value of `post_process` is recommended.

## Installation

Requires yt-dlp `2023.01.02` or above.

You can install this package with pip:

```console
python3 -m pip install -U https://github.com/bradenhilton/yt-dlp-FixupMtime/archive/master.zip
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## Usage

```text
--use-postprocessor FixupMtime[:[mtime_key=<key>];[mtime_format=<format>]]
```

Where `<key>` is the key of your desired datetime within the infojson dictionary and `<format>` is the [format](https://docs.python.org/3.7/library/datetime.html#strftime-and-strptime-behavior) of the datetime.

The default value for the `mtime_key` parameter is `mtime`, which will set the mtime of all files (thumbnails, subtitles etc.) to the existing mtime of the video. If `mtime_key`'s value is `mtime` and the `--mtime` option was passed to yt-dlp at the time of download, the value will be the datetime of the last-modified header.

The default value for the `mtime_format` parameter is `%Y%m%d`. The postprocessor will also attempt to guess the format with yt-dlp's internal list of formats.

Both parameters are optional and can be specified in any order.

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

You can combine multiple invocations, ordered from least to most preferred:

```text
--use-postprocessor FixupMtime:mtime_key=upload_date
--use-postprocessor FixupMtime:mtime_key=release_date
--use-postprocessor FixupMtime:mtime_key=timestamp
--use-postprocessor FixupMtime:mtime_key=release_timestamp
```
