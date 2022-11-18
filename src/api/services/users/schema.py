from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    second_name: str | None = None
    username: str | None = None


class ResponseUser(User):
    class Config:
        orm_mode = True
