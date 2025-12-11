# 🔧 Troubleshooting - Failed to Fetch

## ❌ Error: "Failed to fetch" atau "Tidak bisa terhubung ke server"

### Penyebab Utama:
Backend server **tidak running** atau tidak bisa diakses.

---

## ✅ Solusi Step-by-Step:

### 1. Cek Apakah Backend Running

Buka browser dan akses: `http://localhost:5000/`

**Jika muncul**: "Learnify backend is running 🚀" → ✅ Backend sudah running
**Jika error**: ❌ Backend belum running

### 2. Jalankan Backend Server

Buka **Command Prompt** atau **PowerShell** baru:

```bash
cd C:\xampp\htdocs\Capstone\learning-buddy\learnify-backend
npm install
npm start
```

**Output yang benar:**
```
Server berjalan di port 5000
```

**Biarkan terminal ini tetap terbuka!** Jangan ditutup.

### 3. Cek File .env

Pastikan ada file `.env` di folder `learnify-backend` dengan isi:

```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
PORT=5000
```

### 4. Test Koneksi Backend

Jalankan script check:
```bash
node check_backend.js
```

Atau test manual di browser:
- Buka: `http://localhost:5000/`
- Harus muncul: "Learnify backend is running 🚀"

### 5. Cek Port 5000

Pastikan port 5000 tidak digunakan aplikasi lain:

**Windows:**
```bash
netstat -ano | findstr :5000
```

Jika ada proses lain, tutup atau ubah PORT di `.env`

---

## 🚨 Masalah Lainnya:

### Error: "Cannot find module"
**Solusi:**
```bash
cd learnify-backend
npm install
```

### Error: "EADDRINUSE: address already in use"
**Solusi:** Port 5000 sudah digunakan. Tutup aplikasi lain atau ubah PORT di `.env`

### Error: "Missing SUPABASE_URL"
**Solusi:** Buat file `.env` di folder `learnify-backend` dengan SUPABASE_URL dan SUPABASE_ANON_KEY

### Backend running tapi masih "Failed to fetch"
**Solusi:**
1. Cek browser console (F12) untuk error detail
2. Pastikan URL di `auth/signin.js` dan `auth/signup.js` benar: `http://localhost:5000`
3. Cek firewall/antivirus yang memblokir koneksi

---

## 📝 Checklist Sebelum Sign In/Sign Up:

- [ ] Backend server running (cek `http://localhost:5000/`)
- [ ] File `.env` sudah dibuat di `learnify-backend/`
- [ ] Port 5000 tidak digunakan aplikasi lain
- [ ] Terminal backend tetap terbuka (jangan ditutup)
- [ ] Browser console tidak ada error CORS

---

## 🎯 Quick Fix:

1. **Tutup semua terminal yang running backend**
2. **Buka terminal baru:**
   ```bash
   cd C:\xampp\htdocs\Capstone\learning-buddy\learnify-backend
   npm start
   ```
3. **Tunggu sampai muncul**: "Server berjalan di port 5000"
4. **Buka website lagi** dan coba sign in/sign up

---

## 💡 Tips:

- **Jangan tutup terminal backend** saat menggunakan website
- Jika error masih muncul, **refresh halaman** setelah backend running
- Gunakan **browser console (F12)** untuk melihat error detail

