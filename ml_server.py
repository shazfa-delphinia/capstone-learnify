# ml_server.py

# --- VERCEL REQUIREMENT: Tambahkan Mangum untuk Serverless Function ---
from mangum import Mangum
import os 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional

# --- Import Logika ML Anda ---
# Pastikan jalur import ini benar. 
# Jika file Anda di ml/chatbot_pipeline.py, ini harus berfungsi.
try:
    from ml.chatbot_pipeline import chatbot_pipeline
except ImportError:
    # Ini penting untuk Vercel: jika import gagal, tampilkan error
    print("FATAL ERROR: Tidak dapat mengimpor 'chatbot_pipeline'. Pastikan file ada di 'ml/'.")
    raise

app = FastAPI(
    title="Learnify ML Pipeline API",
    version="1.0.0"
)

# --- KONFIGURASI CORS ---
# Sangat penting agar Frontend (Web) dapat berkomunikasi dengan API
app.add_middleware(
    CORSMiddleware,
    # Mengizinkan semua origin saat development/prototype. 
    # Idealnya, ganti "*" dengan domain Vercel Anda di Production.
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], # Mengizinkan GET, POST, dll.
    allow_headers=["*"],
)

# --- Pydantic Model untuk Validasi Request Body ---
class QuizRequest(BaseModel):
    user_interest_answers: List[str]
    user_tech_answers_mcq: Dict[str, str]
    # Optional field, akan diisi None jika tidak dikirim
    student_id: Optional[str] = None 

# --- Endpoint Health Check (GET) ---
# Endpoint ini akan diakses di https://YOUR-VERCEL-URL.app/api/
@app.get("/")
def read_root():
    """Endpoint untuk memastikan API berjalan"""
    return {"status": "ok", "message": "ML Pipeline API is running successfully on Vercel"}

# --- Endpoint Utama Prediksi (POST) ---
# Endpoint ini akan diakses di https://YOUR-VERCEL-URL.app/api/predict
@app.post("/predict")
async def predict_learning_path(request: QuizRequest):
    """
    Menerima jawaban kuesioner dan MCQ dari user, 
    kemudian mengembalikan rekomendasi learning path dan modul.
    """
    try:
        # Panggil logika utama dari pipeline ML
        result = chatbot_pipeline(
            user_interest_answers=request.user_interest_answers,
            user_tech_answers_mcq=request.user_tech_answers_mcq,
            student_id=request.student_id
        )
        return result
    except Exception as e:
        # Tangkap error, log, dan kembalikan response 500
        # Vercel akan mencatat log ini.
        print(f"Error during ML pipeline execution: {e}") 
        # Untuk keamanan, kita bisa menyembunyikan detail error di Production
        raise HTTPException(
            status_code=500, 
            detail=f"Terjadi kesalahan saat memproses permintaan: {str(e)}"
        )

# --- VERCEL HANDLER ---
# Ini adalah objek yang digunakan Mangum untuk menghubungkan FastAPI dengan 
# lingkungan Serverless Vercel (AWS Lambda). 
# BARIS INI WAJIB ada di akhir file untuk Vercel.
handler = Mangum(app)

# Note: Bagian if __name__ == "__main__": (uvicorn.run) DILARANG keras, 
# karena Vercel tidak menjalankan server persisten. 
# Baris tersebut sudah dihapus dari kode ini.