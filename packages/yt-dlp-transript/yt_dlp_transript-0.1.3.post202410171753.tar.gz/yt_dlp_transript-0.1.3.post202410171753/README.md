# yt-dlp-transript

A handy wrapper for yt-dlp to download transcripts for YouTube videos.

## Usage

    uvx yt-dlp-transript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

Options:

    > ./yt-dlp-transript.py -h
    usage: yt-dlp-transript.py [-h] [-l LANGUAGE] [-v] url

    positional arguments:
      url

    options:
      -h, --help            show this help message and exit
      -l LANGUAGE, --language LANGUAGE
                            subtitles language (default: en)
      -v, --verbose         verbose mode (default: False)

## Requirements

`uv` installed ([docs](https://docs.astral.sh/uv/#getting-started)).
