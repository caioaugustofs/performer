from pydantic import BaseModel


class SocialCommentCreate(BaseModel):
    content: str
    post_id: int
    user_id: int


class SocialCommentPublic(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int

    class Config:
        from_attributes = True


class SocialCommentUpdate(BaseModel):
    content: str
