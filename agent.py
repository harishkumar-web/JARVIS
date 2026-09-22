from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL, require_groq_key
from tools import TOOLS
require_groq_key()
llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.3)

llm_with_tools = llm.bind_tools(TOOLS)

if __name__ == "__main__":

    reply = llm.invoke("Say hello as JARVIS, in one short sentence.")
    print("Plain reply:", reply.content)

    tool_reply = llm_with_tools.invoke("What time is it?")
    print("Tool calls requested:", tool_reply.tool_calls)