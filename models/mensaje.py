from pydantic import BaseModel

class Mensaje(BaseModel):
    to: str
    body: str