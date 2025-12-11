-- =============================================
-- LEARNIFY DATABASE SCHEMA FOR SUPABASE
-- =============================================

-- 1. TABEL USERS
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  email text UNIQUE NOT NULL,
  password text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- 2. TABEL LEARNING PATH (harus dibuat duluan karena jadi referensi)
CREATE TABLE learning_path (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name_lp text NOT NULL,
  summary text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- 3. TABEL KUIS LEARNING PATH
CREATE TABLE lp_quiz_questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question_text text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE lp_quiz_options (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question_id uuid NOT NULL REFERENCES lp_quiz_questions(id) ON DELETE CASCADE,
  option_text text NOT NULL,
  lp_category text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query options by question
CREATE INDEX idx_lp_quiz_options_question ON lp_quiz_options(question_id);

-- 4. TABEL KUIS LEVEL
CREATE TABLE level_quiz_questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tech_category text NOT NULL,
  level text NOT NULL,
  question_text text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE level_quiz_options (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question_id uuid NOT NULL REFERENCES level_quiz_questions(id) ON DELETE CASCADE,
  option_label text,
  option_text text NOT NULL,
  is_correct boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query options by question
CREATE INDEX idx_level_quiz_options_question ON level_quiz_options(question_id);
-- Index untuk filter by tech_category
CREATE INDEX idx_level_quiz_questions_tech ON level_quiz_questions(tech_category);

-- 5. TABEL COURSE
CREATE TABLE course (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  lp_id uuid NOT NULL REFERENCES learning_path(id) ON DELETE CASCADE,
  course_name text NOT NULL,
  level text,
  hours_to_study int,
  course_order int,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query courses by learning path
CREATE INDEX idx_course_lp ON course(lp_id);

-- 6. TABEL TUTORIALS
CREATE TABLE tutorials (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id uuid NOT NULL REFERENCES course(id) ON DELETE CASCADE,
  title text NOT NULL,
  tutorial_order int,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query tutorials by course
CREATE INDEX idx_tutorials_course ON tutorials(course_id);

-- 7. TABEL USER LEARNING PATH RESULT
CREATE TABLE user_learning_path_result (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  recommended_lp uuid REFERENCES learning_path(id) ON DELETE SET NULL,
  total_score int,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query by user
CREATE INDEX idx_user_lp_result_user ON user_learning_path_result(user_id);

-- 8. TABEL USER LEVEL RESULT
CREATE TABLE user_level_result (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  learning_path uuid REFERENCES learning_path(id) ON DELETE SET NULL,
  level text,
  score int,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query by user
CREATE INDEX idx_user_level_result_user ON user_level_result(user_id);

-- 9. TABEL USER ROADMAP
CREATE TABLE user_roadmap (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  lp_id uuid REFERENCES learning_path(id) ON DELETE SET NULL,
  user_level text,
  generated_at timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query by user
CREATE INDEX idx_user_roadmap_user ON user_roadmap(user_id);

-- 10. TABEL USER PROGRESS
CREATE TABLE user_progress (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tutorial_id uuid REFERENCES tutorials(id) ON DELETE SET NULL,
  status text CHECK (status IN ('not_started', 'in_progress', 'completed')) DEFAULT 'not_started',
  progress_percentage int DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Index untuk query by user
CREATE INDEX idx_user_progress_user ON user_progress(user_id);
-- Unique constraint: 1 user hanya punya 1 progress per tutorial
CREATE UNIQUE INDEX idx_user_progress_unique ON user_progress(user_id, tutorial_id);

-- =============================================
-- TRIGGER UNTUK AUTO UPDATE updated_at
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger ke semua tabel
CREATE TRIGGER tr_users_updated BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_learning_path_updated BEFORE UPDATE ON learning_path FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_lp_quiz_questions_updated BEFORE UPDATE ON lp_quiz_questions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_lp_quiz_options_updated BEFORE UPDATE ON lp_quiz_options FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_level_quiz_questions_updated BEFORE UPDATE ON level_quiz_questions FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_level_quiz_options_updated BEFORE UPDATE ON level_quiz_options FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_course_updated BEFORE UPDATE ON course FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_tutorials_updated BEFORE UPDATE ON tutorials FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_user_lp_result_updated BEFORE UPDATE ON user_learning_path_result FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_user_level_result_updated BEFORE UPDATE ON user_level_result FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_user_roadmap_updated BEFORE UPDATE ON user_roadmap FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_user_progress_updated BEFORE UPDATE ON user_progress FOR EACH ROW EXECUTE FUNCTION update_updated_at();
