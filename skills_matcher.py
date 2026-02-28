from skills import SKILLS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_skills(resume_text):
    found_skills = []
    for skills in SKILLS:
        if skills in resume_text:
            found_skills.append(skills)
    return list(set(found_skills))

def calculate_match_score(resume_text, job_description):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_description])

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(similarity[0][0] * 100, 2)


print("Skills match Successful Run")


