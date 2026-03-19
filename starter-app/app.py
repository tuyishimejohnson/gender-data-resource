import streamlit as st
from src.loaders import load_all_data
from src.agent.agent import ask

@st.cache_data
def get_data():
    return load_all_data()

studies, resources, quality = get_data()

st.set_page_config(page_title="Gender Data Visibility Starter", layout="wide")

st.title("Gender Data Visibility Starter App")
st.write(
    "This starter is a runnable baseline for hackathon teams. "
    "Use the sidebar pages for discovery, dashboard views, and data quality checks."
)
question = st.chat_input("Ask a question")
if question:
    with st.spinner("Thinking..."):
        response = ask(question, studies, quality)
    st.markdown(response)


