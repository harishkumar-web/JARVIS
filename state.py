from typing import Annotated, Optional, TypedDict
from langgraph.graph.message import add_messages
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_request: str
    plan: list
    tool_results: list
    memories: list
    current_task: str
    iteration_count: int
    final_response: str
    pending_confirmation: Optional[dict]
    confirmed: bool