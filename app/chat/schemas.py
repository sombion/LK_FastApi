from pydantic import BaseModel, Field


class SSendMessages(BaseModel):
    text_message: str = Field(...)
    id_chat: int = Field(...)