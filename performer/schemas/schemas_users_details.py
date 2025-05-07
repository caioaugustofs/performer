from pydantic import BaseModel


class UserDetailAdd(BaseModel):
    id: int
