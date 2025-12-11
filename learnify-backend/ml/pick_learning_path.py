from collections import Counter
from ml.config import interest_to_lp, tech_to_lp

def pick_learning_path(interest_cat, tech_cats):
    candidates_interest = interest_to_lp.get(interest_cat, []) if interest_cat else []
    candidates_tech = []
    for t in tech_cats:
        candidates_tech.extend(tech_to_lp.get(t, []))

    counter = Counter()
    for lp in candidates_interest:
        counter[lp] += 2
    for lp in candidates_tech:
        counter[lp] += 1

    if not counter:
        return None, []

    ranked = counter.most_common()
    top_score = ranked[0][1]
    top_lps = [lp for lp, sc in ranked if sc == top_score]

    intersection = list(set(candidates_interest) & set(candidates_tech))
    if intersection:
        inter_scores = sorted([(lp, counter[lp]) for lp in intersection], key=lambda x: x[1], reverse=True)
        chosen = inter_scores[0][0]
        return chosen, ranked

    return top_lps[0], ranked
