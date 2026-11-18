import tempfile
from pathlib import Path

import gradio as gr

from transcribe import format_segments, transcribe

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7860
MAX_UPLOAD_SIZE = "1gb"
CONCURRENT_JOBS = 1
CACHE_CLEANUP_INTERVAL_SECONDS = 3600
CACHE_MAX_AGE_SECONDS = 86400


def handle_upload(audio_path: str | None) -> tuple[str, str]:
    if not audio_path:
        raise gr.Error("Pilih file audio dulu.")
    try:
        segments = transcribe(Path(audio_path))
    except RuntimeError as error:
        raise gr.Error("File tidak bisa dibaca sebagai audio.") from error
    if not segments:
        raise gr.Error("Tidak ada suara yang terdeteksi di file ini.")

    text = format_segments(segments)
    output_path = Path(tempfile.mkdtemp()) / f"{Path(audio_path).stem}.txt"
    output_path.write_text(text, encoding="utf-8")
    return text, str(output_path)


with gr.Blocks(
    title="Transa",
    delete_cache=(CACHE_CLEANUP_INTERVAL_SECONDS, CACHE_MAX_AGE_SECONDS),
) as demo:
    gr.Markdown("# Transa\nUpload rekaman, tunggu prosesnya, lalu salin atau unduh teksnya.")
    audio_input = gr.File(label="File audio", file_types=["audio"])
    submit_button = gr.Button("Transkripsi", variant="primary")
    text_output = gr.Textbox(label="Hasil", lines=20, buttons=["copy"])
    file_output = gr.File(label="Unduh .txt")

    submit_button.click(handle_upload, inputs=audio_input, outputs=[text_output, file_output])


if __name__ == "__main__":
    demo.queue(default_concurrency_limit=CONCURRENT_JOBS).launch(
        server_name=SERVER_HOST,
        server_port=SERVER_PORT,
        max_file_size=MAX_UPLOAD_SIZE,
    )
