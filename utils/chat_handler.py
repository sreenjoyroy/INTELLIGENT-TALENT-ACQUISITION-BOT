import streamlit as st
from utils.session_state_handler import get_session_data, update_chat_history
from llm_utils.local_llm_runner import run_local_llm  # Assuming this is how you call Mistral
def chatbot_interface(user_input: str):
    from langchain.agents import initialize_agent, AgentType
    from langchain.llms import Ollama  # Or your LLM wrapper

    llm = Ollama(model="mistral")  # or whatever you're using

    # agent = initialize_agent(
    #     tools=[],  # Empty is okay with CHAT_ZERO_SHOT
    #     llm=llm,
    #     agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True
    # )
    response = llm(user_input)

    return response

def process_user_input(user_input: str):
    session_data = get_session_data()
    history = session_data.get("chat_history", [])

    # Build context (simple example - customize as needed)
    context = "\n".join([f"User: {turn['user']}\nBot: {turn['bot']}" for turn in history])

    # Call the local LLM with context
    prompt = f"{context}\nUser: {user_input}\nBot:"
    response = run_local_llm(prompt)  # Your wrapper around Ollama/Mistral

    update_chat_history(user_input, response)
    return response
