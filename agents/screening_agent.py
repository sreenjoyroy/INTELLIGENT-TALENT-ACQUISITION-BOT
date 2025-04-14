from crewai import Agent, Task, Crew
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Dict
from llm_utils.local_llm_runner import load_mistral_7b
from chroma_db.db_handler import get_latest_hr_entry, get_latest_applicant_entry

# -------------------------
# 📦 Data models
# -------------------------
class HRData(BaseModel):
    job_description: Optional[str] = Field(default=None, description="HR's job requirements")

class ApplicantData(BaseModel):
    resume_text: Optional[str] = Field(default=None, description="Applicant's resume content")

# -------------------------
# 🛠 Tool 1: Fetch HR + Applicant data
# -------------------------
def fetch_latest_entries() -> Dict[str, BaseModel]:
    hr_data_raw = get_latest_hr_entry() or {}
    applicant_data_raw = get_latest_applicant_entry() or {}
    return {
        "hr": HRData(**hr_data_raw),
        "applicant": ApplicantData(**applicant_data_raw)
    }

class FetchLatestEntriesTool(BaseTool):
    name: str = Field(default="fetch_records", frozen=True)
    description: str = Field(
        default="Retrieves latest HR job post and applicant resume from database",
        frozen=True
    )

    def _run(self) -> str:  # Removed unused query parameter
        data = fetch_latest_entries()
        return f"""
        HR Job Description: {data['hr'].job_description or 'Not available'}
        Applicant Resume: {data['applicant'].resume_text or 'Not available'}
        """

# -------------------------
# 🛠 Tool 2: Analyze Resume
# -------------------------
class AnalyzeResumeTool(BaseTool):
    name: str = Field(default="analyze_fitment", frozen=True)
    description: str = Field(
        default="Evaluates resume against job requirements using keyword analysis",
        frozen=True
    )

    def _run(self) -> str:  # Fixed method signature
        data = fetch_latest_entries()
        hr = data["hr"]
        applicant = data["applicant"]

        if not hr.job_description or not applicant.resume_text:
            return "Error: Missing required data for analysis"

        job_desc = hr.job_description.lower()
        resume = applicant.resume_text.lower()

        required_skills = {"python", "sql", "machine learning"}  # Example skills
        found_skills = [skill for skill in required_skills if skill in resume]
        
        match_percentage = len(found_skills) / len(required_skills) * 100
        return f"""
        📊 Match Analysis:
        - Required Skills: {', '.join(required_skills)}
        - Found Skills: {', '.join(found_skills) or 'None'}
        - Match Percentage: {match_percentage:.1f}%
        """

# -------------------------
# 🤖 Screening Agent Class
# -------------------------
class ScreeningAgent:
    def __init__(self):  # Fixed constructor
        self.llm = load_mistral_7b()
        self.agent = self._create_agent()

    def _create_agent(self):
        return Agent(
            role="AI Recruitment Specialist",
            goal="Accurately match candidates to job requirements",
            backstory=(
                "A cutting-edge AI recruiter with advanced NLP capabilities, "
                "specializing in technical candidate evaluation and job matching."
            ),
            tools=[
                FetchLatestEntriesTool().model_dump(),
                AnalyzeResumeTool().model_dump()
            ],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=5  # Prevent infinite loops
        )

    def create_screening_task(self):
        return Task(
            description=(
                "Analyze the applicant's resume against the HR's job description. "
                "Consider technical skills, experience duration, and keyword matches. "
                "Provide a detailed report with final eligibility decision."
            ),
            expected_output=(
                "## Screening Report\n"
                "1. Skill Match Percentage\n"
                "2. Missing Requirements\n"
                "3. Final Recommendation\n"
                "4. Suggested Interview Questions"
            ),
            agent=self.agent
        )

# -------------------------
# 🚀 Main Runner
# -------------------------
def run_screening_agent():
    screening = ScreeningAgent()
    task = screening.create_screening_task()
    
    crew = Crew(
        agents=[screening.agent],
        tasks=[task],
        verbose=2,
        memory=True
    )

    return crew.kickoff()

if __name__ == "__main__":
    result = run_screening_agent()
    print(f"🔍 Screening Results:\n{result}")