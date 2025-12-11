# Setup Instructions untuk Learnify

## 1. Backend Setup (Node.js)

```bash
cd learnify-backend
npm install
```

Buat file `.env` di folder `learnify-backend`:
```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
PORT=5000
```

Jalankan backend:
```bash
npm start
# atau untuk development
npm run dev
```

Backend akan berjalan di `http://localhost:5000`

## 2. Machine Learning Server Setup (Python)

Install dependencies:
```bash
pip install -r requirements.txt
```

Jalankan ML server:
```bash
python ml_server.py
```

ML server akan berjalan di `http://localhost:8000`

## 3. Frontend

Buka `index.html` di browser atau gunakan web server (XAMPP sudah menyediakan).

## 4. Database Setup

Jalankan SQL schema di Supabase:
- Buka file `learnify-backend/database/schema.sql`
- Copy semua SQL dan jalankan di Supabase SQL Editor

## 5. Testing

1. **Sign Up**: Buka `auth/signup.html` dan buat akun baru
2. **Sign In**: Buka `auth/signin.html` dan login dengan akun yang sudah dibuat
3. **Profile**: Setelah login, profile akan menampilkan nama dan email user
4. **ML Pipeline**: Backend endpoint `/quiz/ml/predict` siap digunakan untuk memprediksi learning path

## API Endpoints

### Authentication
- `POST /auth/register` - Register user baru
- `POST /auth/login` - Login user

### Quiz & ML
- `POST /quiz/ml/predict` - Prediksi learning path menggunakan ML
  Body:
  ```json
  {
    "user_interest_answers": ["answer1", "answer2"],
    "user_tech_answers_mcq": {
      "question1": "answer1",
      "question2": "answer2"
    },
    "student_id": "optional"
  }
  ```

## Troubleshooting

1. **Backend tidak bisa connect ke Supabase**: Pastikan `.env` sudah diisi dengan benar
2. **ML server error**: Pastikan file CSV ada di folder `Data/` dengan nama yang benar
3. **Login tidak berfungsi**: Pastikan backend server sudah running di port 5000
4. **Profile tidak muncul**: Pastikan localStorage memiliki data `userName` dan `userEmail` setelah login

