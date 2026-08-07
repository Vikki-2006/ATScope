import pytest
from fastapi.testclient import TestClient
from main import app
from app.services.parser import ResumeParser
from app.services.ats_analyzer import ATSAnalyzer
from app.services.job_matcher import JobMatcher
from app.services.report_generator import ReportGenerator

client = TestClient(app)

def test_landing_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Resume" in response.text

def test_auth_flow():
    # Register test user
    email = "testuser@example.com"
    pwd = "password123"
    reg_res = client.post("/api/v1/auth/register", json={
        "full_name": "Test Candidate",
        "email": email,
        "password": pwd
    })
    # Allowed to succeed (201) or return 400 if already created in previous run
    assert reg_res.status_code in [201, 400]

    # Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": pwd
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    assert token is not None

def test_parser_and_scoring():
    sample_text = """
    Jane Doe
    jane.doe@example.com | (555) 123-4567 | linkedin.com/in/janedoe | github.com/janedoe
    
    Professional Summary
    Senior Software Engineer with 5+ years of experience in Python, FastAPI, React, PostgreSQL, Docker, AWS, and Machine Learning.
    
    Work Experience
    Senior Engineer | Acme Corp (2021 - Present)
    - Architected microservices reducing latency by 45%.
    - Built real-time analytics pipelines processing over 1M events daily.
    
    Education
    B.S. Computer Science | University of Technology
    
    Skills
    Python, FastAPI, Django, React, TypeScript, PostgreSQL, Redis, Docker, Kubernetes, AWS, PyTorch, Git
    """
    
    parsed = ResumeParser.parse_text(sample_text)
    assert parsed["name"] == "Jane Doe"
    assert parsed["email"] == "jane.doe@example.com"
    assert "Python" in parsed["skills"] or "python" in [s.lower() for s in parsed["skills"]]

    # ATS Scoring
    scores = ATSAnalyzer.analyze(parsed)
    assert scores["ats_score"] > 60.0
    assert scores["formatting_score"] > 50.0

    # Job Matcher
    jd = "Looking for a Senior Python Developer with FastAPI, PostgreSQL, Docker, AWS, and Kubernetes experience."
    match = JobMatcher.match(sample_text, parsed["skills"], jd)
    assert match["match_score"] > 60.0
    assert len(match["matched_skills"]) > 0

def test_pdf_report_generator():
    sample_analysis = {
        "job_title": "Senior Backend Developer",
        "overall_score": 88.5,
        "ats_score": 92.0,
        "formatting_score": 90.0,
        "readability_score": 85.0,
        "keyword_match_score": 86.0,
        "skill_match_score": 90.0,
        "experience_score": 85.0,
        "education_score": 90.0,
        "project_score": 80.0,
        "matched_skills": ["Python", "FastAPI", "Docker", "PostgreSQL"],
        "missing_skills": ["Redis", "AWS"],
        "recommended_skills": ["Kubernetes", "GraphQL"],
        "suggestions_json": {
            "improve_summary": ["Add high impact metric."],
            "bullet_points": ["Use XYZ formula."]
        }
    }
    
    pdf_bytes = ReportGenerator.generate_pdf_report(sample_analysis, "Jane Doe")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
