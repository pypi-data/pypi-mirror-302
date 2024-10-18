# yt-dlp-transript

A handy wrapper for yt-dlp to download transcripts for YouTube videos.

## Usage

    uvx yt-dlp-transript https://www.youtube.com/watch?v=dQw4w9WgXcQ

or
    pip install yt-dlp-transript
    yt-dlp-transript https://www.youtube.com/watch?v=dQw4w9WgXcQ

## Options:

    > yt-dlp-transript -h
    usage: yt-dlp-transript [-h] [-l LANGUAGE] [-v] url

    positional arguments:
      url                   Youtube URL

    options:
      -h, --help            show this help message and exit
      -l LANGUAGE, --language LANGUAGE
                            subtitles language (default: en)
      -v, --verbose         verbose mode (default: False)
