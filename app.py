import streamlit as st
import plotly.graph_objects as go
from resume_pars import extract_text_from_pdf, clean_text
from skills_matcher import extract_skills, calculate_match_score

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main title with gradient animation */
    .main-title {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: shine 3s linear infinite;
    }

    @keyframes shine {
        to {
            background-position: 200% center;
        }
    }

    /* Subtitle styling */
    .sub-title {
        color: #4a5568;
        font-size: 1.2rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }

    /* Glass morphism card */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
        transition: transform 0.3s;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.15);
    }

    /* Metric cards with neon glow */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.8rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.7s;
    }

    .metric-card:hover::before {
        left: 100%;
    }

    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }

    .metric-label {
        color: white;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }

    .metric-value {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
    }

    .metric-sublabel {
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Skill tags with hover effect */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s;
        cursor: default;
        border: 1px solid rgba(255,255,255,0.2);
    }

    .skill-tag:hover {
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
    }

    /* Section headers with animated underline */
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2d3748;
        margin: 2rem 0 1.5rem 0;
        position: relative;
        display: inline-block;
    }

    .section-header::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 60%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
        animation: slide 2s ease-in-out infinite;
    }

    @keyframes slide {
        0%, 100% { width: 60%; }
        50% { width: 100%; }
    }

    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.05);
    }

    /* Text area styling */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s;
    }

    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f6f9fc 0%, #edf2f7 100%);
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    /* Progress bar styling */
    .stProgress .st-bo {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }

    /* Floating animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .floating {
        animation: float 3s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# Header with animated icon
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-title">📄 AI Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Intelligent resume screening powered by NLP & Machine Learning</p>',
                unsafe_allow_html=True)

# Sidebar with features
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span style="font-size: 3rem;" class="floating">⚡</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 Features")

    features = [
        ("📄 PDF Parsing", "Extract text from PDF resumes"),
        ("🔍 Skill Extraction", "Identify technical & soft skills"),
        ("📊 Match Scoring", "Calculate resume-job fit"),
        ("🎯 Gap Analysis", "Identify missing keywords"),
        ("📈 Visual Analytics", "Interactive skill visualization")
    ]

    for icon, desc in features:
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 0.8rem; border-radius: 10px; margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">{icon}</span><br>
            <span style="font-size: 0.9rem; color: #718096;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Tips section
    with st.expander("💡 Pro Tips"):
        st.markdown("""
        - Use clean, text-based PDFs
        - Include both technical & soft skills
        - Match job description keywords
        - Update resume regularly
        """)

# Main content area with glass morphism
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# Input section in two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📤 Upload Resume")
    uploaded_resume = st.file_uploader(
        "Choose PDF file",
        type=["pdf"],
        help="Upload resume in PDF format (max 10MB)"
    )

    if uploaded_resume:
        st.success(f"✅ Loaded: {uploaded_resume.name}")

with col2:
    st.markdown("### 📝 Job Description")
    job_desc = st.text_area(
        "Paste job description here",
        height=150,
        placeholder="Paste the job description text here..."
    )

st.markdown('</div>', unsafe_allow_html=True)

# Analysis section
if uploaded_resume and job_desc:
    with st.spinner("🔄 Analyzing resume... Please wait"):
        # Extract and process
        resume_text = extract_text_from_pdf(uploaded_resume)
        cleaned_resume = clean_text(resume_text)
        skills_found = extract_skills(cleaned_resume)
        match_score = calculate_match_score(cleaned_resume, job_desc.lower())

        # Calculate additional metrics
        job_words = set(job_desc.lower().split())
        resume_words = set(cleaned_resume.lower().split())
        keyword_match = len(resume_words.intersection(job_words))
        total_keywords = len(job_words)
        keyword_percentage = (keyword_match / total_keywords * 100) if total_keywords > 0 else 0

    # Metrics dashboard
    st.markdown('<h2 class="section-header">📊 Analysis Dashboard</h2>', unsafe_allow_html=True)

    # First row - main metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Match Score</div>
            <div class="metric-value">{match_score:.1f}%</div>
            <div class="metric-sublabel">Resume-Job Fit</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);">
            <div class="metric-label">Skills Found</div>
            <div class="metric-value">{len(skills_found)}</div>
            <div class="metric-sublabel">Technical & Soft Skills</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
            <div class="metric-label">Keyword Match</div>
            <div class="metric-value">{keyword_match}</div>
            <div class="metric-sublabel">Out of {total_keywords}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #9f7aea 0%, #b794f4 100%);">
            <div class="metric-label">Resume Length</div>
            <div class="metric-value">{len(resume_words)}</div>
            <div class="metric-sublabel">Unique Words</div>
        </div>
        """, unsafe_allow_html=True)

    # Progress bar for match score
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 Match Score Analysis")
    col_progress, col_score = st.columns([3, 1])
    with col_progress:
        st.progress(match_score / 100)
    with col_score:
        if match_score >= 80:
            st.success("🌟 Excellent Match!")
        elif match_score >= 60:
            st.warning("📊 Good Match")
        elif match_score >= 40:
            st.info("📝 Average Match")
        else:
            st.error("⚠️ Needs Improvement")

    # Skills section with visual tags
    st.markdown('<h2 class="section-header">🔍 Skills Analysis</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🎯 Extracted Skills")

        if skills_found:
            # Create skill tags HTML
            skills_html = ""
            for skill in sorted(skills_found)[:30]:  # Limit to 30 skills
                skills_html += f'<span class="skill-tag">{skill}</span>'

            if len(skills_found) > 30:
                skills_html += f'<span class="skill-tag">+{len(skills_found) - 30} more</span>'

            st.markdown(f'<div style="margin: 1rem 0;">{skills_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No skills detected")

    with col2:
        # Skill distribution gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=len(skills_found),
            title={'text': "Skill Count"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 15], 'color': "#fed7d7"},
                    {'range': [15, 30], 'color': "#feebc8"},
                    {'range': [30, 50], 'color': "#c6f6d5"}
                ]
            }
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)

    # Gap Analysis
    st.markdown('<h2 class="section-header">🎯 Gap Analysis</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Matching Keywords")
        matching_keywords = resume_words.intersection(job_words)
        if matching_keywords:
            matching_html = ""
            for kw in sorted(matching_keywords)[:20]:
                matching_html += f'<span class="skill-tag" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">{kw}</span>'
            if len(matching_keywords) > 20:
                matching_html += f'<span class="skill-tag">+{len(matching_keywords) - 20} more</span>'
            st.markdown(f'<div>{matching_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No matching keywords found")

    with col2:
        st.markdown("### ❌ Missing Keywords")
        missing_keywords = job_words - resume_words
        if missing_keywords:
            missing_html = ""
            for kw in sorted(missing_keywords)[:20]:
                missing_html += f'<span class="skill-tag" style="background: linear-gradient(135deg, #f56565 0%, #c53030 100%);">{kw}</span>'
            if len(missing_keywords) > 20:
                missing_html += f'<span class="skill-tag">+{len(missing_keywords) - 20} more</span>'
            st.markdown(f'<div>{missing_html}</div>', unsafe_allow_html=True)
        else:
            st.success("✅ No missing keywords!")

    # Improvement suggestions
    st.markdown('<h2 class="section-header">💡 Improvement Suggestions</h2>', unsafe_allow_html=True)

    if missing_keywords:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("""
        ### 📝 Recommendations:
        1. **Add missing keywords** to your resume
        2. **Quantify achievements** with metrics
        3. **Highlight relevant experience** matching job description
        4. **Use industry-standard terminology**
        """)

        # Show top missing keywords to add
        top_missing = list(missing_keywords)[:5]
        if top_missing:
            st.markdown("**Top keywords to include:**")
            missing_rec_html = ""
            for kw in top_missing:
                missing_rec_html += f'<span class="skill-tag" style="background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);">{kw}</span>'
            st.markdown(f'<div>{missing_rec_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("🎉 Your resume is well-aligned with the job description!")

    # Download report option
    st.markdown("---")
    col_download1, col_download2, col_download3 = st.columns([1, 2, 1])
    with col_download2:
        report_data = f"""Resume Analysis Report
Match Score: {match_score:.1f}%
Skills Found: {len(skills_found)}
Skills: {', '.join(skills_found)}
Matching Keywords: {', '.join(matching_keywords) if matching_keywords else 'None'}
Missing Keywords: {', '.join(missing_keywords) if missing_keywords else 'None'}
"""
        st.download_button(
            label="📥 Download Analysis Report",
            data=report_data,
            file_name="resume_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    # Interactive placeholder when no input
    st.markdown("""
    <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #f6f9fc 0%, #edf2f7 100%); border-radius: 20px; margin: 2rem 0;">
        <span style="font-size: 5rem;" class="floating">📄</span>
        <h2 style="color: #2d3748; margin: 1rem 0;">Ready to analyze resumes?</h2>
        <p style="color: #718096; font-size: 1.1rem;">Upload a resume and paste job description to get started</p>
    </div>
    """, unsafe_allow_html=True)

    # Features preview
    st.markdown('<h2 class="section-header">✨ Key Features</h2>', unsafe_allow_html=True)

    feat_col1, feat_col2, feat_col3 = st.columns(3)

    with feat_col1:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem;">🎯</span>
            <h3>Smart Matching</h3>
            <p style="color: #718096;">AI-powered resume-job fit analysis</p>
        </div>
        """, unsafe_allow_html=True)

    with feat_col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem;">🔍</span>
            <h3>Skill Extraction</h3>
            <p style="color: #718096;">Automatic detection of technical skills</p>
        </div>
        """, unsafe_allow_html=True)

    with feat_col3:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem;">📊</span>
            <h3>Visual Analytics</h3>
            <p style="color: #718096;">Interactive dashboards and insights</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #718096; font-size: 0.9rem; padding: 2rem 0;">
    <p>Powered by NLP & Machine Learning | Built with Streamlit | 📄 AI Resume Analyzer v2.0</p>
    <p style="margin-top: 0.5rem; font-size: 0.8rem;">© 2024 AI Resume Analyzer. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
