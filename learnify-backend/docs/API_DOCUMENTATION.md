# Learnify API Documentation

Base URL: `http://localhost:5000`

---

## 1. Authentication

### POST /auth/register
Mendaftarkan user baru.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "optional123"
}
```

**Response (201):**
```json
{
  "message": "Register berhasil",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**Error (409):**
```json
{
  "error": "Email sudah terdaftar"
}
```

---

### POST /auth/login
Login dengan email.

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response (200):**
```json
{
  "message": "Login berhasil",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

**Error (404):**
```json
{
  "error": "User tidak ditemukan"
}
```

---

## 2. Learning Path Quiz

### GET /quiz/lp/questions
Mengambil semua pertanyaan LP quiz beserta opsi jawaban.

**Response (200):**
```json
{
  "questions": [
    {
      "id": "uuid",
      "question_text": "Apa yang paling kamu minati?",
      "lp_quiz_options": [
        {
          "id": "uuid",
          "option_text": "Membuat website",
          "lp_category": "Web Development"
        },
        {
          "id": "uuid",
          "option_text": "Membuat aplikasi mobile",
          "lp_category": "Mobile Development"
        }
      ]
    }
  ]
}
```

---

### POST /quiz/lp/submit
Submit jawaban LP quiz dan dapatkan rekomendasi learning path.

**Request Body:**
```json
{
  "user_id": "uuid",
  "answers": [
    { "question_id": "uuid", "selected_option_id": "uuid" },
    { "question_id": "uuid", "selected_option_id": "uuid" }
  ]
}
```

**Response (200):**
```json
{
  "message": "Quiz LP berhasil disubmit",
  "result": {
    "id": "uuid",
    "user_id": "uuid",
    "recommended_lp": "uuid",
    "total_score": 5,
    "category_scores": {
      "Web Development": 3,
      "Mobile Development": 2
    },
    "recommended_category": "Web Development"
  }
}
```

---

## 3. Level Quiz

### GET /quiz/level/questions
Mengambil soal level quiz berdasarkan kategori teknologi.

**Query Parameters:**
- `tech_category` (optional): Filter berdasarkan kategori (e.g., "JavaScript", "Python")
- `level` (optional): Filter berdasarkan level (e.g., "beginner", "intermediate")

**Example:** `/quiz/level/questions?tech_category=JavaScript`

**Response (200):**
```json
{
  "questions": [
    {
      "id": "uuid",
      "tech_category": "JavaScript",
      "level": "beginner",
      "question_text": "Apa output dari console.log(typeof null)?",
      "level_quiz_options": [
        { "id": "uuid", "option_label": "A", "option_text": "null" },
        { "id": "uuid", "option_label": "B", "option_text": "object" },
        { "id": "uuid", "option_label": "C", "option_text": "undefined" }
      ]
    }
  ]
}
```

---

### POST /quiz/level/submit
Submit jawaban level quiz dan dapatkan hasil level.

**Request Body:**
```json
{
  "user_id": "uuid",
  "learning_path_id": "uuid",
  "answers": [
    { "question_id": "uuid", "selected_option_id": "uuid" },
    { "question_id": "uuid", "selected_option_id": "uuid" }
  ]
}
```

**Response (200):**
```json
{
  "message": "Quiz level berhasil disubmit",
  "result": {
    "id": "uuid",
    "user_id": "uuid",
    "learning_path": "uuid",
    "level": "intermediate",
    "score": 70,
    "correct_answers": 7,
    "total_questions": 10
  }
}
```

**Level ditentukan berdasarkan score:**
- 0-49%: beginner
- 50-79%: intermediate
- 80-100%: advanced

---

## 4. Learning Path & Course

### GET /learning-paths
Mengambil semua learning path.

**Response (200):**
```json
{
  "learning_paths": [
    {
      "id": "uuid",
      "name_lp": "Web Development",
      "summary": "Belajar membuat website dari dasar",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

### GET /learning-paths/:id
Mengambil detail satu learning path.

**Response (200):**
```json
{
  "learning_path": {
    "id": "uuid",
    "name_lp": "Web Development",
    "summary": "Belajar membuat website dari dasar",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

---

### GET /learning-paths/:id/courses
Mengambil semua course dalam satu learning path.

**Response (200):**
```json
{
  "courses": [
    {
      "id": "uuid",
      "lp_id": "uuid",
      "course_name": "HTML & CSS Fundamentals",
      "level": "beginner",
      "hours_to_study": 10,
      "course_order": 1
    },
    {
      "id": "uuid",
      "lp_id": "uuid",
      "course_name": "JavaScript Basics",
      "level": "beginner",
      "hours_to_study": 15,
      "course_order": 2
    }
  ]
}
```

---

### GET /courses/:id/tutorials
Mengambil semua tutorial dalam satu course.

**Response (200):**
```json
{
  "tutorials": [
    {
      "id": "uuid",
      "course_id": "uuid",
      "title": "Pengenalan HTML",
      "tutorial_order": 1
    },
    {
      "id": "uuid",
      "course_id": "uuid",
      "title": "Struktur Dasar HTML",
      "tutorial_order": 2
    }
  ]
}
```

---

## 5. User Progress

### GET /user/:id/progress
Mengambil progress belajar user.

**Response (200):**
```json
{
  "progress": [
    {
      "id": "uuid",
      "status": "completed",
      "progress_percentage": 100,
      "updated_at": "2024-01-01T00:00:00Z",
      "tutorials": {
        "id": "uuid",
        "title": "Pengenalan HTML",
        "tutorial_order": 1,
        "course": {
          "id": "uuid",
          "course_name": "HTML & CSS Fundamentals",
          "level": "beginner",
          "learning_path": {
            "id": "uuid",
            "name_lp": "Web Development"
          }
        }
      }
    }
  ]
}
```

---

### POST /user/progress/update
Update progress tutorial user.

**Request Body:**
```json
{
  "user_id": "uuid",
  "tutorial_id": "uuid",
  "status": "in_progress",
  "progress_percentage": 50
}
```

**Status options:** `not_started`, `in_progress`, `completed`

**Response (200):**
```json
{
  "message": "Progress berhasil diupdate",
  "progress": {
    "id": "uuid",
    "user_id": "uuid",
    "tutorial_id": "uuid",
    "status": "in_progress",
    "progress_percentage": 50,
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

---

## 6. User Roadmap

### GET /user/:id/roadmap
Mengambil roadmap belajar user.

**Response (200):**
```json
{
  "roadmaps": [
    {
      "id": "uuid",
      "user_level": "beginner",
      "generated_at": "2024-01-01T00:00:00Z",
      "learning_path": {
        "id": "uuid",
        "name_lp": "Web Development",
        "summary": "Belajar membuat website",
        "course": [
          {
            "id": "uuid",
            "course_name": "HTML & CSS",
            "level": "beginner",
            "hours_to_study": 10,
            "course_order": 1,
            "tutorials": [
              { "id": "uuid", "title": "Intro HTML", "tutorial_order": 1 }
            ]
          }
        ]
      }
    }
  ]
}
```

---

### POST /user/roadmap/generate
Membuat roadmap baru untuk user (hasil rekomendasi chatbot).

**Request Body:**
```json
{
  "user_id": "uuid",
  "lp_id": "uuid",
  "user_level": "beginner"
}
```

**Response (201):**
```json
{
  "message": "Roadmap berhasil dibuat",
  "roadmap": {
    "id": "uuid",
    "user_level": "beginner",
    "generated_at": "2024-01-01T00:00:00Z",
    "learning_path": {
      "id": "uuid",
      "name_lp": "Web Development",
      "summary": "Belajar membuat website"
    }
  }
}
```

---

## 7. User Results

### GET /user/:id/lp-results
Mengambil hasil LP quiz user.

**Response (200):**
```json
{
  "results": [
    {
      "id": "uuid",
      "total_score": 5,
      "created_at": "2024-01-01T00:00:00Z",
      "learning_path": {
        "id": "uuid",
        "name_lp": "Web Development"
      }
    }
  ]
}
```

---

### GET /user/:id/level-results
Mengambil hasil level quiz user.

**Response (200):**
```json
{
  "results": [
    {
      "id": "uuid",
      "level": "intermediate",
      "score": 70,
      "created_at": "2024-01-01T00:00:00Z",
      "learning_path": {
        "id": "uuid",
        "name_lp": "Web Development"
      }
    }
  ]
}
```

---

## 8. Chat (AI)

### POST /chat
Kirim pesan ke AI chatbot.

**Request Body:**
```json
{
  "message": "Apa itu JavaScript?"
}
```

**Response (200):**
```json
{
  "reply": "JavaScript adalah bahasa pemrograman..."
}
```

---

## Error Responses

Semua endpoint mengembalikan format error yang konsisten:

```json
{
  "error": "Pesan error"
}
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request (parameter tidak lengkap)
- `404` - Not Found
- `409` - Conflict (data sudah ada)
- `500` - Internal Server Error
