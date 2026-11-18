# Transa

Ubah rekaman audio menjadi teks, **100% lokal** di Mac (tidak ada audio yang dikirim ke internet).
Memakai model Whisper `large-v3-turbo` lewat [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper), yang berjalan di GPU Apple Silicon.

## Prasyarat

| Kebutuhan | Minimal |
|---|---|
| Mac | Apple Silicon (M1 atau lebih baru). Mac Intel **tidak bisa** |
| macOS | 26 atau lebih baru (syarat versi MLX yang dikunci di `uv.lock`) |
| RAM | 8 GB (cukup untuk 1 transkripsi sekaligus) |
| Disk kosong | ± 5 GB (dependensi 1,3 GB + model 1,5 GB + ruang untuk file upload) |
| Internet | Hanya saat instalasi dan run pertama (unduh model) |

## Instalasi (sekali saja)

**1. Install Homebrew** (lewati jika `brew --version` sudah jalan). Ikuti petunjuk di https://brew.sh

**2. Install `uv` dan `ffmpeg`**

```bash
brew install uv ffmpeg
```

- `uv`: mengelola Python dan dependensi project. Python 3.12 akan diunduh otomatis, jadi tidak perlu install Python sendiri.
- `ffmpeg`: membaca berbagai format audio (mp3, m4a, wav, dll.).

**3. Masuk ke folder project lalu install dependensi**

```bash
cd "/path/ke/transa"
uv sync
```

**4. Unduh model** (± 1,5 GB, disimpan di `~/.cache/huggingface`)

```bash
uv run python -c "import huggingface_hub, transcribe; huggingface_hub.snapshot_download(transcribe.MODEL_REPO)"
```

- Perintah ini mengunduh model sesuai `MODEL_REPO` di `transcribe.py`. Jika model sudah ada, tidak diunduh ulang.
- Langkah ini opsional. Jika dilewati, model diunduh otomatis saat transkripsi pertama (transkripsi pertama jadi lama).
- Setelah model terunduh, aplikasi bisa berjalan **tanpa internet**.

## Menjalankan UI web

```bash
caffeinate -i uv run app.py
```

- Buka **http://localhost:7860** di browser Mac ini.
- `caffeinate -i` mencegah Mac sleep selama proses berjalan. Hentikan server dengan `Ctrl + C`.

### Akses dari laptop lain (Wi-Fi yang sama)

1. Cek IP Mac:
   ```bash
   ipconfig getifaddr en0
   ```
2. Rekan kerja membuka `http://<ip-tadi>:7860`, misalnya `http://192.168.1.20:7860`.
3. Saat pertama kali jalan, jika macOS bertanya *"Allow incoming network connections?"* untuk Python, pilih **Allow**.

Job diproses **satu per satu**. User lain otomatis masuk antrian dan bisa melihat posisinya di layar.

## Menjalankan lewat terminal (tanpa UI)

```bash
uv run transcribe.py rekaman.m4a > hasil.txt
```

Teks hasil masuk ke `hasil.txt`. Durasi audio, waktu proses, dan kecepatan (x realtime) tampil di terminal.

## Pengaturan

Semua pengaturan berupa konstanta di bagian atas file:

| Konstanta | File | Default | Keterangan |
|---|---|---|---|
| `MODEL_REPO` | `transcribe.py` | `mlx-community/whisper-large-v3-turbo` | Model Whisper yang dipakai |
| `DEFAULT_LANGUAGE` | `transcribe.py` | `id` | Bahasa audio |
| `SERVER_PORT` | `app.py` | `7860` | Port UI web |
| `MAX_UPLOAD_SIZE` | `app.py` | `1gb` | Batas ukuran file upload |
| `CONCURRENT_JOBS` | `app.py` | `1` | Jumlah job paralel. Naikkan hanya jika RAM ≥ 16 GB |
| `CACHE_MAX_AGE_SECONDS` | `app.py` | `86400` (1 hari) | File upload dan hasil di cache dihapus setelah umur ini |

## Struktur project

```
transa/
├── app.py           # UI web (Gradio): upload, antrian, hasil, unduh .txt
├── transcribe.py    # Inti transkripsi + CLI
├── pyproject.toml   # Daftar dependensi
├── uv.lock          # Versi dependensi yang dikunci
└── .python-version  # Python 3.12
```

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `File tidak bisa dibaca sebagai audio` | File rusak atau bukan audio. Cek apakah `ffmpeg` terpasang: `ffmpeg -version` |
| `Address already in use` / port 7860 terpakai | Cari prosesnya dengan `lsof -i :7860`, lalu tutup prosesnya, atau ganti `SERVER_PORT` |
| Proses sangat lambat / Mac lag | Tutup aplikasi berat lain (browser dengan banyak tab, dll.). RAM 8 GB cukup sesak |
| Transkripsi pertama lama sekali | Normal, model 1,5 GB sedang diunduh |
| Laptop lain tidak bisa membuka halaman | Pastikan satu jaringan Wi-Fi, IP benar, dan firewall macOS mengizinkan Python |
| `uv sync` gagal di instalasi MLX | Pastikan Mac Apple Silicon dan macOS 26+ |

## Catatan keamanan

- **Belum ada login.** Siapa pun di jaringan yang sama bisa memakai aplikasi ini. Jangan jalankan di Wi-Fi publik (kafe, bandara).
- Hasil transkripsi tiap user tidak terlihat oleh user lain, dan hilang jika tab browser ditutup. Simpan atau unduh hasilnya dulu.
- Rekaman yang di-upload disimpan sementara di cache Gradio dan dihapus otomatis setelah 1 hari.
