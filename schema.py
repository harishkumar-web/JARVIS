from pydantic import BaseModel, Field
class RouterDecision(BaseModel):
    needs_tools: bool = Field(
        description="True if answering the request requires calling a tool."
    )
    reasoning: str = Field(
        description="One short sentence explaining the decision."
    )
if __name__ == "__main__":
    from config import require_groq_key, GROQ_MODEL, GROQ_API_KEY
    from langchain_groq import ChatGroq

    require_groq_key()
    llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
    structured_llm = llm.with_structured_output(RouterDecision)

    result = structured_llm.invoke("What's the weather in Pune?")
    print(result)
    assert isinstance(result, RouterDecision)