from collections import defaultdict
import pandas as pd

def evaluate_tech_mcq(tech_q_df, user_tech_answers):
    # Handle different possible column names
    question_col = None
    tech_cat_col = None
    correct_answer_col = None
    
    for col in tech_q_df.columns:
        col_lower = col.lower()
        if 'question' in col_lower or 'desc' in col_lower:
            question_col = col
        if 'tech_category' in col_lower or ('tech' in col_lower and 'cat' in col_lower):
            tech_cat_col = col
        if 'correct' in col_lower or 'answer' in col_lower:
            correct_answer_col = col
    
    if question_col is None:
        raise ValueError(f"Could not find question column. Available: {tech_q_df.columns.tolist()}")
    
    tech_scores = defaultdict(int)
    correct_count = 0
    total_answered = 0

    for _, row in tech_q_df.iterrows():
        q = row[question_col]
        tech_cat = row.get(tech_cat_col, "Unknown") if tech_cat_col else "Unknown"
        if q in user_tech_answers:
            chosen = str(user_tech_answers[q]).strip()
            total_answered += 1
            correct_ans = str(row[correct_answer_col]).strip() if correct_answer_col else ""
            if chosen and correct_ans and chosen == correct_ans:
                tech_scores[tech_cat] += 1
                correct_count += 1
            else:
                tech_scores[tech_cat] += 0

    percent_correct = (correct_count / total_answered * 100) if total_answered > 0 else None
    ranked = sorted(tech_scores.items(), key=lambda x: x[1], reverse=True)
    categories_ranked = [t for t, s in ranked]
    return categories_ranked, dict(tech_scores), percent_correct
