"""Prototype: transkripsi satu file audio secara lokal dengan mlx-whisper (GPU Apple Silicon).

Pemakaian:
    uv run transcribe.py <file-audio> [--language id]
"""

import argparse
import sys
import time
from pathlib import Path

import mlx_whisper

MODEL_REPO = "mlx-community/whisper-large-v3-turbo"
DEFAULT_LANGUAGE = "id"
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60


def format_timestamp(seconds: float) -> str:
    """Ubah detik menjadi HH:MM:SS."""
    total = int(seconds)
    hours, rest = divmod(total, SECONDS_PER_HOUR)
    minutes, secs = divmod(rest, SECONDS_PER_MINUTE)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_segments(segments: list[dict]) -> str:
    """Gabungkan segmen menjadi teks, satu baris per segmen dengan timestamp."""
    return "\n".join(
        f"[{format_timestamp(seg['start'])} - {format_timestamp(seg['end'])}] {seg['text']}"
        for seg in segments
    )


def transcribe(audio_path: Path, language: str = DEFAULT_LANGUAGE) -> list[dict]:
    """Transkripsi audio menjadi daftar segmen {start, end, text, speaker}.

    `speaker` selalu None untuk sekarang; disiapkan agar diarization (pyannote)
    nanti cukup mengisi field ini tanpa mengubah bentuk data.
    """
    result = mlx_whisper.transcribe(
        str(audio_path), path_or_hf_repo=MODEL_REPO, language=language
    )
    return [
        {"start": seg["start"], "end": seg["end"], "text": seg["text"].strip(), "speaker": None}
        for seg in result["segments"]
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Transkripsi audio ke teks secara lokal.")
    parser.add_argument("audio", type=Path, help="Path file audio (mp3, m4a, wav, dll.)")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help="Kode bahasa (default: id)")
    args = parser.parse_args()

    if not args.audio.is_file():
        print(f"File tidak ditemukan: {args.audio}", file=sys.stderr)
        return 1

    started = time.perf_counter()
    try:
        segments = transcribe(args.audio, args.language)
    except RuntimeError as error:
        print(f"Gagal memproses audio: {error}", file=sys.stderr)
        return 1
    elapsed = time.perf_counter() - started

    print(format_segments(segments))

    audio_seconds = segments[-1]["end"] if segments else 0
    speed = audio_seconds / elapsed if elapsed else 0
    print(
        f"\nDurasi audio ~{format_timestamp(audio_seconds)} | waktu proses {elapsed:.1f} detik"
        f" | {speed:.1f}x realtime",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
