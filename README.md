# yt-dlp-FixupMtime

A [yt-dlp](https://github.com/yt-dlp/yt-dlp) postprocessor [plugin](https://github.com/yt-dlp/yt-dlp#plugins) which sets the mtime of all files to a given datetime value by key.

NOTE: This postprocessor should not be run before files are downloaded.

## Installation

Requires yt-dlp `2023.01.02` or above.

You can install this package with pip:

```console
python3 -m pip install -U https://github.com/bradenhilton/yt-dlp-FixupMtime/archive/master.zip
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## Usage

Pass `--use-postprocessor FixupMtime:mtime_key=<key>`, replacing `<key>` with your chosen key to activate the postprocessor e.g. `--use-postprocessor FixupMtime:mtime_key=upload_date`.
