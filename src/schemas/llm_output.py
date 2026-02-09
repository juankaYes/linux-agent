
# schemas/llm_output.py
from pydantic import BaseModel, Field
from typing import Literal

class LLMOrchestrationOutput(BaseModel):
    intent: Literal["troubleshooting", "teaching"] | None = Field(description="The intent of the user input")
    # confidence: Literal["high", "low"]
    # risk_level: Literal["low", "medium", "high"]
    needs_clarification: Literal[True, False] = Field(description="Whether the user input is unclear or ambiguous or has nothing to do with linux systems")
    cleaned_query: str | None = Field(description="A cleaned version of the user input that is more consistent and focused on linux system issues")

def parse_llm_output(output: str) -> LLMOrchestrationOutput:
    """Parse the LLM output into a structured format."""
    import json
    try:
        data = json.loads(output)
        return LLMOrchestrationOutput(**data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM output: {e}")
    

class LLMTroubleshootingOutput(BaseModel):
    command: dict[str, str] = Field(description="The commands that have been executed by the agent, with the command as the key and the output as the value")
    next_steps: str = Field(description="The next steps to solve the problem based on the command outputs")
    request: str = Field(description="A request or question to ask the user if more information is needed to solve the problem or suggestion")