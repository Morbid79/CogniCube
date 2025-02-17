from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., description="User id")
    password: str = Field(..., description="User password")
    email: str = Field(..., description="User email")
    created_at: str = Field(..., description="User creation date")
    email_verified: bool = Field(False, description="Email verification status")

class User(UserBase):
    id: int = Field(..., description="User id")

    class Config:
        orm_mode = True
