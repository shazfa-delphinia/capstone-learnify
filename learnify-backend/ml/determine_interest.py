from collections import defaultdict
import pandas as pd

def determine_interest_category(interest_q_df, user_interest_answers):
    # Handle different possible column names
    option_col = None
    category_col = None
    
    for col in interest_q_df.columns:
        col_lower = col.lower()
        if 'option' in col_lower or 'text' in col_lower:
            option_col = col
        if 'category' in col_lower or 'cat' in col_lower:
            category_col = col
    
    if option_col is None or category_col is None:
        raise ValueError(f"Could not find required columns. Available: {interest_q_df.columns.tolist()}")
    
    opt_to_cat = dict(zip(interest_q_df[option_col], interest_q_df[category_col]))
    scores = defaultdict(int)
    for ans in user_interest_answers:
        cat = opt_to_cat.get(ans)
        if cat:
            scores[cat] += 1
    if not scores:
        return None, {}
    best = max(scores, key=scores.get)
    return best, dict(scores)
