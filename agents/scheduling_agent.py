from crewai import Agent, Task, Crew
from llm_utils.local_llm_runner import load_mistral_7b
from chroma_db.db_handler import get_latest_hr_entry, get_latest_applicant_entry
from email_utils.send_email import send_email_to_hr, send_email_to_applicant
from langchain.tools import BaseTool
from typing import Optional
from pydantic import BaseModel

# -------------------------
# 📦 Pydantic Models
# -------------------------
class HRData(BaseModel):
    email: Optional[str] = None

class ApplicantData(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None

# -------------------------
# 🛠️ Tool 1: Fetch Interview Data
# -------------------------
class FetchInterviewDataTool(BaseTool):
    name : str = "FetchInterviewData"
    description : str = "Fetch the latest HR and Applicant data from the database."

    def _run(self, query: str = "") -> str:
        try:
            hr_data_raw = get_latest_hr_entry()
            applicant_data_raw = get_latest_applicant_entry()
            hr_data = HRData(**hr_data_raw) if hr_data_raw else HRData()
            applicant_data = ApplicantData(**applicant_data_raw) if applicant_data_raw else ApplicantData()
            return (
                f"Fetched HR: {hr_data.email}\n"
                f"Applicant: {applicant_data.name}, {applicant_data.email}, "
                f"{applicant_data.position} at {applicant_data.company}"
            )
        except Exception as e:
            return f"❌ Error fetching interview data: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")

# -------------------------
# 🛠️ Tool 2: Schedule Interview + Notify
# -------------------------
class ScheduleInterviewTool(BaseTool):
    name : str = "ScheduleInterviewAndNotify"
    description : str = "Schedule the interview and notify both HR and the applicant via email."

    def _run(self, query: str = "") -> str:
        try:
            hr_data_raw = get_latest_hr_entry()
            applicant_data_raw = get_latest_applicant_entry()
            hr_info = HRData(**hr_data_raw) if hr_data_raw else HRData()
            applicant_info = ApplicantData(**applicant_data_raw) if applicant_data_raw else ApplicantData()

            hr_email = hr_info.email
            applicant_email = applicant_info.email
            candidate_name = applicant_info.name
            job_role = applicant_info.position
            company = applicant_info.company

            if not all([hr_email, applicant_email, candidate_name, job_role, company]):
                return "❌ Missing required information for scheduling."

            interview_link = "https://meet.google.com/test-interview-link"
            proposed_slot = "Tomorrow at 11:00 AM IST"

            hr_confirmed = send_email_to_hr(hr_email, candidate_name, proposed_slot, interview_link)
            if not hr_confirmed:
                return f"⏳ Waiting for HR ({hr_email}) to confirm interview."

            send_email_to_applicant(applicant_email, candidate_name, job_role, company, proposed_slot, interview_link)
            return f"✅ Interview scheduled for {candidate_name} with {company} at {proposed_slot}."

        except Exception as e:
            return f"❌ Error in scheduling interview: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")

# -------------------------
# 🤖 Scheduling Agent Class
# -------------------------
class SchedulingAgent:
    def __init__(self):
        self.llm = load_mistral_7b()
        self.agent = self._create_agent()

    def _create_agent(self):
        return Agent(
            role="Interview Scheduler",
            goal="Schedule interviews and coordinate with HR and applicants",
            backstory=(
                "A smart assistant that ensures interviews are scheduled smoothly by fetching required data, "
                "notifying HR for confirmation, and then informing the applicant."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[FetchInterviewDataTool(), ScheduleInterviewTool()]
        )

    def create_scheduling_task(self):
        return Task(
            description=(
                "Fetch the latest HR and applicant information, then schedule the interview. "
                "Start by confirming the time with HR via email. Once HR confirms, notify the applicant."
            ),
            expected_output="Confirmation of whether the interview is scheduled and notifications sent.",
            agent=self.agent
        )

# -------------------------
# 🚀 Run the Scheduling Agent
# -------------------------
def run_scheduling_agent():
    scheduler = SchedulingAgent()
    task = scheduler.create_scheduling_task()
    
    crew = Crew(
        agents=[scheduler.agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
    status = run_scheduling_agent()
    print(f"📆 Interview Scheduling Result:\n{status}")
