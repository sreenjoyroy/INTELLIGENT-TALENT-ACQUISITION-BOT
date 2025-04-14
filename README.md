# 🤖 Intelligent Talent Acquisition Assistant

A fully autonomous AI-driven recruitment assistant designed to simplify and optimize the hiring process for HR teams. This end-to-end platform uses conversational AI, LLM agents, and local vector databases to automate candidate sourcing, resume analysis, applicant engagement, and interview scheduling.

## 🚀 Key Features

- **Local LLM Integration**: Powered by Mistral-7B via Ollama for offline processing.
- **Autonomous AI Agents**:
  - 🧠 Screening Agent
  - 💬 Engagement Agent
  - 📅 Scheduling Agent
- **Interactive HR Chatbot**: Built with Streamlit for real-time HR interaction.
- **Email Notifications**: Sends templated engagement and interview emails.
- **CrewAI & Langchain**: Agentic AI orchestration for parallel task handling.
- **ChromaDB**: For storing HR and applicant data securely and locally.

## 🛠 Tech Stack

- **Frontend**: Streamlit / React (optional)
- **Backend**: Python 3.12.4, Langchain, CrewAI
- **Database**: ChromaDB / Pinecone (optional)
- **LLM**: Mistral 7B via Ollama (fully local)
- **Email**: Gmail OAuth / SendGrid Integration

## 📂 Project Structure

├── agents/ ├── email_utils/ ├── llm_utils/ ├── chroma_db/ ├── styles/ ├── app.py ├── style.css ├── .gitignore └── README.md


## 🔐 Security

- Environment variables are stored in `.env` and excluded from Git tracking.
- Virtual environments like `Sreenjoy` are also excluded for clean collaboration.

## 📧 Contact

Built with 💡 by [Sreenjoy Roy].  
For inquiries, reach out at [bijoyroykgp2@gmail.com] or connect via [LinkedIn](https://www.linkedin.com/in/sreenjoy-roy-a22b0226b/)