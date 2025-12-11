# Dockerfile

# Menggunakan Python base image yang lebih kecil dan stabil
FROM python:3.12-slim

# Menetapkan direktori kerja di dalam container
WORKDIR /app

# Menyalin file requirements.txt dan menginstal dependensi
# Menggunakan --no-cache-dir untuk mengurangi ukuran image akhir
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode proyek Anda ke dalam container
# Termasuk ml_server.py, folder ml/, dan file statis lainnya
COPY . .

# Environment variable untuk memberitahu FastAPI bahwa ini adalah container
ENV PORT 8080

# Mendefinisikan perintah yang akan dijalankan saat container dimulai.
# Kita akan menggunakan Gunicorn untuk menjalankan Uvicorn/FastAPI secara production-ready.
# Uvicorn harus ada di requirements.txt Anda (yang sudah ada).
# Nama modulnya: [nama file python]:[nama objek FastAPI]
# Di kasus Anda: ml_server:app
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker ml_server:app