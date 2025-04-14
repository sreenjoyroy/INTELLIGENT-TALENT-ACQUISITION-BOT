from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.agents import initialize_agent, AgentType

# Load local Mistral model via Ollama
def load_mistral_7b():
    llm = Ollama(model="mistral", temperature=0.3)
    return llm

# Initialize LangChain agent
def create_agent(llm):
    tools = []
    agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent

# Define different prompt templates
def get_prompt_template(mode: str):
    templates = {
        "chat": "You are a helpful assistant.\n\n{user_input}",
        "screening": "You're a resume screening assistant.\nEvaluate this:\n\n{user_input}",
        "engagement": "Generate a friendly follow-up to engage the candidate:\n\n{user_input}",
        "scheduling": "Draft a professional scheduling response with the following info:\n\n{user_input}",
        "custom": "{user_input}"
    }
    return templates.get(mode, templates["custom"])

# Run prompt through the local LLM
def run_local_llm(prompt: str, mode: str = "chat") -> str:
    try:
        llm = load_mistral_7b()
        agent = create_agent(llm)
        template = get_prompt_template(mode)
        final_prompt = template.format(user_input=prompt)
        response = agent.run(final_prompt)
        return response.strip()
    except Exception as e:
        return f"⚠️ LLM Error: {str(e)}"

# For CLI test
if __name__ == "__main__":
    test_prompt = "Generate a thank you message for an applicant who just completed the screening round."
    output = run_local_llm(test_prompt, mode="engagement")
    print("LLM Output:", output)
