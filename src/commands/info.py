

from pydantic import BaseModel, Field


class CommandOutput(BaseModel):
    command     : str = Field(..., description="The command that was executed")
    result      : str = Field(..., description="The output of the command")
    is_error    : bool = Field(..., description="Indicates if the command failed")