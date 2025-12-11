import express from "express";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import csv from "csv-parser";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const router = express.Router();

// Helper untuk membaca CSV
function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(filePath)
      .pipe(csv())
      .on("data", (data) => results.push(data))
      .on("end", () => resolve(results))
      .on("error", (error) => reject(error));
  });
}

// GET /quiz/csv/interest/questions - Ambil pertanyaan interest dari CSV
router.get("/csv/interest/questions", async (req, res) => {
  try {
    // Path relatif dari learnify-backend ke Data folder
    const csvPath = path.join(process.cwd(), "..", "Data", "Resource Data Learning Buddy - Current Interest Questions.csv");
    
    if (!fs.existsSync(csvPath)) {
      return res.status(404).json({ error: "File CSV tidak ditemukan" });
    }

    const data = await readCSV(csvPath);
    
    // Group by question_desc
    const questionsMap = {};
    data.forEach((row) => {
      const question = row.question_desc || row.question;
      if (!questionsMap[question]) {
        questionsMap[question] = {
          question_text: question,
          options: [],
        };
      }
      questionsMap[question].options.push({
        option_text: row.option_text || row.option,
        category: row.category,
      });
    });

    const questions = Object.values(questionsMap);

    res.json({ questions });
  } catch (error) {
    console.error("Get interest questions error:", error);
    res.status(500).json({ error: "Gagal mengambil pertanyaan interest" });
  }
});

// GET /quiz/csv/tech/questions - Ambil pertanyaan tech dari CSV
router.get("/csv/tech/questions", async (req, res) => {
  try {
    const { tech_category, difficulty } = req.query;
    // Path relatif dari learnify-backend ke Data folder
    const csvPath = path.join(process.cwd(), "..", "Data", "Resource Data Learning Buddy - Current Tech Questions.csv");
    
    if (!fs.existsSync(csvPath)) {
      return res.status(404).json({ error: "File CSV tidak ditemukan" });
    }

    let data = await readCSV(csvPath);
    
    // Filter by tech_category if provided
    if (tech_category) {
      data = data.filter((row) => 
        (row.tech_category || "").toLowerCase() === tech_category.toLowerCase()
      );
    }
    
    // Filter by difficulty if provided
    if (difficulty) {
      data = data.filter((row) => 
        (row.difficulty || "").toLowerCase() === difficulty.toLowerCase()
      );
    }

    // Group by difficulty (level) and take max 10 per level
    const questionsByLevel = {};
    
    // First, group all questions by level
    const allQuestionsByLevel = {};
    data.forEach((row) => {
      const level = (row.difficulty || row.Difficulty || "").toLowerCase().trim();
      if (!level || level === "" || level === "unknown") return; // Skip if no difficulty
      
      if (!allQuestionsByLevel[level]) {
        allQuestionsByLevel[level] = [];
      }
      
      const questionText = row.question_desc || row.question || row.Question;
      if (!questionText || questionText.trim() === "") return; // Skip if no question text
      
      const options = [
        { label: "A", text: row.option_1 || row.Option_1 },
        { label: "B", text: row.option_2 || row.Option_2 },
        { label: "C", text: row.option_3 || row.Option_3 },
        { label: "D", text: row.option_4 || row.Option_4 },
      ].filter((opt) => opt.text && opt.text.trim() !== ""); // Remove empty options
      
      // Only add if we have at least 2 options
      if (options.length >= 2) {
        // Check for duplicates
        const isDuplicate = allQuestionsByLevel[level].some(
          q => q.question_text === questionText
        );
        
        if (!isDuplicate) {
          allQuestionsByLevel[level].push({
            question_text: questionText,
            tech_category: row.tech_category || row.Tech_Category,
            difficulty: row.difficulty || row.Difficulty,
            options: options,
            correct_answer: row.correct_answer || row.Correct_Answer,
          });
        }
      }
    });
    
    // Now, for each level, shuffle and take max 5
    Object.keys(allQuestionsByLevel).forEach((level) => {
      const levelQuestions = allQuestionsByLevel[level];
      
      // Shuffle questions for this level
      for (let i = levelQuestions.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [levelQuestions[i], levelQuestions[j]] = [levelQuestions[j], levelQuestions[i]];
      }
      
      // Take max 10 questions from this level
      questionsByLevel[level] = levelQuestions.slice(0, 10);
    });

    // Flatten all questions from all levels into one array
    const questions = [];
    Object.keys(questionsByLevel).forEach((level) => {
      questions.push(...questionsByLevel[level]);
    });

    console.log(`\n=== Tech Quiz Questions Selection ===`);
    console.log(`Total questions selected: ${questions.length}`);
    console.log(`Total levels found: ${Object.keys(questionsByLevel).length}`);
    console.log(`Questions per level:`);
    Object.keys(questionsByLevel).forEach((level) => {
      const count = questionsByLevel[level].length;
      console.log(`  - ${level}: ${count}/10 questions`);
    });
    console.log(`=====================================\n`);

    // Shuffle final questions to randomize order across levels
    for (let i = questions.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [questions[i], questions[j]] = [questions[j], questions[i]];
    }

    res.json({ questions });
  } catch (error) {
    console.error("Get tech questions error:", error);
    res.status(500).json({ error: "Gagal mengambil pertanyaan tech" });
  }
});

export default router;

