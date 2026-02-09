from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_input: str
    intent: Optional[str]
    needs_clarification: Optional[bool]
    cleaned_query: Optional[str]
    response: Optional[str]
