import os
import json
import pandas as pd
from collections import defaultdict, Counter

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "Data")

PATH_INTEREST_Q = os.path.join(DATA_DIR, "Resource Data Learning Buddy - Current Interest Questions.csv")
PATH_TECH_Q = os.path.join(DATA_DIR, "Resource Data Learning Buddy - Current Tech Questions.csv")
PATH_MODULES_JSON = os.path.join(DATA_DIR, "roadmap.json")

def load_csv(path):
    return pd.read_csv(path)

def load_modules(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

interest_to_lp = {
    "Mobile Development": ["Android Developer", "iOS Developer", "Multi-Platform App Developer"],
    "Artificial Intelligence": ["AI Engineer", "Data Scientist", "Gen AI Engineer"],
    "Cloud Computing": ["Google Cloud Professional", "DevOps Engineer"],
    "Web Development": ["Front-End Web Developer", "React Developer", "Back-End Developer JavaScript"],
}

tech_to_lp = {
    "Android": ["Android Developer"],
    "iOS": ["iOS Developer"],
    "Machine Learning": ["AI Engineer", "Data Scientist"],
    "Cloud Computing": ["Google Cloud Professional"],
    "Web": ["Front-End Web Developer", "Back-End Developer JavaScript"],
    "Data": ["Data Scientist"],
}

