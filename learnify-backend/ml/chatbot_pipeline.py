from ml.config import PATH_INTEREST_Q, PATH_TECH_Q, PATH_MODULES_JSON, load_csv, load_modules
from ml.determine_interest import determine_interest_category
from ml.evaluate_tech import evaluate_tech_mcq
from ml.determine_level import determine_json_level_from_percent
from ml.pick_learning_path import pick_learning_path
from ml.filter_modules import filter_modules_by_lp_and_level

def chatbot_pipeline(user_interest_answers, user_tech_answers_mcq, student_id=None,
                     path_interest_q=PATH_INTEREST_Q, path_tech_q=PATH_TECH_Q,
                     path_modules_json=PATH_MODULES_JSON):
    interest_q_df = load_csv(path_interest_q)
    tech_q_df = load_csv(path_tech_q)
    modules = load_modules(path_modules_json)

    interest_cat, interest_scores = determine_interest_category(interest_q_df, user_interest_answers)
    tech_cats_ranked, tech_scores, percent_correct = evaluate_tech_mcq(tech_q_df, user_tech_answers_mcq)
    level = determine_json_level_from_percent(percent_correct)
    chosen_lp, lp_ranked = pick_learning_path(interest_cat, tech_cats_ranked)
    filtered_modules = filter_modules_by_lp_and_level(modules, chosen_lp, level)

    return {
        "student_id": student_id,
        "interest_category": interest_cat,
        "interest_scores": interest_scores,
        "tech_categories_ranked": tech_cats_ranked,
        "tech_scores": tech_scores,
        "tech_percent_correct": percent_correct,
        "detected_level": level,
        "chosen_learning_path": chosen_lp,
        "lp_ranked_scores": lp_ranked,
        "modules_filtered": filtered_modules
    }
