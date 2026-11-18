# Changelog

Semua perubahan penting pada project ini dicatat di file ini.

Format mengikuti [Keep a Changelog](https://keepachangelog.com/id-ID/1.1.0/),
dan versi mengikuti [Semantic Versioning](https://semver.org/lang/id/).

## [Unreleased]

## [0.1.0] - 2026-11-18

### Added

- Transkripsi audio ke teks secara lokal memakai `mlx-whisper` dengan model `whisper-large-v3-turbo` (GPU Apple Silicon), default Bahasa Indonesia.
- CLI `transcribe.py` yang menampilkan hasil per segmen dengan timestamp, plus durasi audio, waktu proses, dan kecepatan (x realtime).
- Field `speaker` pada setiap segmen (masih `None`) sebagai persiapan fitur pembeda pembicara.
- UI web `app.py` (Gradio): upload file, antrian 1 job sekaligus, tombol copy hasil, dan unduh `.txt`.
- Akses UI dari laptop lain di jaringan yang sama (port `7860`).
- Batas upload 1 GB dan penghapusan otomatis file upload/hasil di cache setelah 1 hari.
- Pesan error untuk upload kosong, file yang bukan audio, dan audio tanpa suara.
- README berisi instalasi, cara unduh model, cara menjalankan, pengaturan, dan troubleshooting.
