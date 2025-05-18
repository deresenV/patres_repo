from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserResponse):
    pass
