from crewai import Agent, Task, Crew
from llm_utils.local_llm_runner import load_mistral_7b
from chroma_db.db_handler import get_latest_applicant_entry
from email_utils.send_email import send_engagement_email
from langchain.tools import BaseTool
from pydantic import BaseModel
from typing import Optional


# -------------------------
# 📦 Applicant Info Model
# -------------------------
class ApplicantInfo(BaseModel):
    name: Optional[str] = "Candidate"
    position: Optional[str] = "the position"
    email: Optional[str] = "applicant@example.com"


# -------------------------
# 🛠️ Tool 1: Generate Engagement Message Tool
# -------------------------
class GenerateEngagementMessageTool(BaseTool):
    name : str = "GenerateEngagementMessage"
    description : str = "Generate a friendly email message to engage the applicant and ask for availability."

    def _run(self, query: str = "") -> str:
        try:
            applicant_data = get_latest_applicant_entry()
            applicant = ApplicantInfo(**applicant_data)

            return (
                f"Hi {applicant.name},\n\n"
                f"Thank you for applying for {applicant.position}. "
                f"We have reviewed your profile and would love to know more about you!\n"
                f"Could you please share your availability for a quick chat or interview?\n\n"
                f"Best regards,\nTalent Acquisition Team"
            )
        except Exception as e:
            return f"❌ Failed to generate engagement message: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")


# -------------------------
# 🛠️ Tool 2: Send Engagement Email Tool
# -------------------------
class SendEngagementEmailTool(BaseTool):
    name : str = "SendEngagementEmail"
    description : str = "Send a follow-up email to the applicant encouraging them to respond."

    def _run(self, query: str = "") -> str:
        try:
            # Format: "email;name"
            email, name = query.split(";")
            send_engagement_email(email.strip(), name.strip())
            return f"✅ Engagement email sent to {name.strip()} at {email.strip()}."
        except Exception as e:
            return f"❌ Failed to send engagement email: {e}"

    def _arun(self, query: str):
        raise NotImplementedError("Async not supported.")


# -------------------------
# 🤖 Engagement Agent Class
# -------------------------
class EngagementAgent:
    def __init__(self):
        self.llm = load_mistral_7b()
        self.agent = self._create_agent()

    def _create_agent(self):
        return Agent(
            role="Candidate Engagement Specialist",
            goal="Keep candidates engaged and collect their availability",
            backstory="You specialize in sending friendly and timely messages to candidates to maintain interest and collect availability.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[GenerateEngagementMessageTool(), SendEngagementEmailTool()]
        )

    def create_engagement_task(self):
        return Task(
            description=(
                "Fetch the latest applicant data. Generate a friendly message and send a follow-up "
                "email asking for their availability for the next step."
            ),
            expected_output="A personalized message sent to the applicant requesting availability.",
            agent=self.agent
        )


# -------------------------
# 🚀 Run Engagement Agent
# -------------------------
def run_engagement_agent():
    agent = EngagementAgent()
    task = agent.create_engagement_task()

    crew = Crew(
        agents=[agent.agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    return result


if __name__ == "__main__":
    message = run_engagement_agent()
    print(f"\n💬 Engagement Message Sent:\n{message}")
