from pathlib import Path
from subprocess import run
from typing import Any, Dict
import json

import typer
from pytube import Stream, YouTube, Playlist
from pytube.cli import on_progress

from rich.console import Console

console = Console()


def _yt_info(yt: YouTube) -> Dict[str, Any]:
    return {
        "title": yt.title,
        "description": yt.description,
        "author": yt.author,
        "publish_date": str(yt.publish_date),
        "id": yt.video_id,
    }


def main():
    ffmpeg_installed = run(["which", "ffmpeg"], capture_output=True)
    if ffmpeg_installed.returncode != 0:
        raise RuntimeError(
            "ffmpeg not installed, install ffmpeg and ensure it's on your $PATH"
        )
    p = Playlist("https://www.youtube.com/playlist?list=PLYXaKIsOZBsu3h2SSKEovRn7rGy7wkUAV")
    for yt in p.videos:
        info = _yt_info(yt)
        _id = info["id"]
        output_path: Path = Path("data") / _id / "raw"
        output_path.mkdir(parents=True, exist_ok=True)
        Path(output_path / "info.json").write_text(json.dumps(info))

        # audio stream with lowest bitrate
        audio_stream: Stream = min(
            yt.streams.filter(only_audio=True), key=lambda s: int(s.abr[:-4])
        )
        audio_filename = "audio." + audio_stream.default_filename.split(".")[-1]
        with console.status(f"Downloading Audio: {info['title']}"):
            audio_stream.download(output_path=str(output_path), filename=audio_filename)

        with console.status(f"Converting Audio: {info['title']}"):
            run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(output_path / audio_filename),
                    # Reduce to Mono
                    "-ac",
                    "1",
                    # Sample rate = 16000 Hz
                    "-ar",
                    "16000",
                    str(output_path / "audio.wav"),
                ],
                capture_output=True,
            )


if __name__ == "__main__":
    main()
