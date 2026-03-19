import pandas as pd
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from src.agent.context import build_context_string, prompt

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-5")

chain = prompt | llm


def ask(question: str, studies: pd.DataFrame, quality: pd.DataFrame) -> str:
    context = build_context_string(studies, quality, question)
    result = chain.invoke({"question": question, "studies_context": context})
    print(result.content)
    return result.content
