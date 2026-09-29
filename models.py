from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, description="نام کاربر")
    age: int = Field(..., ge=0, le=120, description="سن کاربر")


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    age: int | None = Field(None, ge=0, le=120)


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
