from pydantic import BaseModel, Field

class User(BaseModel):
    """User model"""

    id: int = Field(..., description="User id")
    name: str = Field(..., description="User name")
    phone: str = Field(..., description="User phone")
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    created_at: str = Field(..., description="User creation date")