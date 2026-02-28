import streamlit as st
from resume_pars import extract_text_from_pdf, clean_text
from skills_matcher import extract_skills, calculate_match_score

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("AI Resume Analyzer")
st.write("Analyze resumes using NLP & Machine learning")

st.divider()

## Upload Resume
uploaded_resume = st.file_uploader("Upload resume (pdf)", ["pdf"])


## Job Description
job_desc = st.text_area("Paste Job Description here")

if uploaded_resume and job_desc:
    with st.spinner("Press it Analyzing Resume"):
        resume_text = extract_text_from_pdf(uploaded_resume)
        cleaned_resume = clean_text(resume_text)

        skills_found = extract_skills(cleaned_resume)
        match_score = calculate_match_score(cleaned_resume, job_desc.lower())

    st.subheader("Analysis Resume")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"match Score : {match_score}")

    with col2:
        st.info(f"Fills Found : {len(skills_found)}")

    st.subheader("Extract skills")
    st.write(", ".join(skills_found))

    missing_skills = [
        skill for skill in job_desc.lower().split()
        if skill in skills_found
    ]

    st.subheader("Missing / Weak Area")
    st.write("Improve keywords related to job description")

else:
    st.info("Please upload resume and enter job description")

