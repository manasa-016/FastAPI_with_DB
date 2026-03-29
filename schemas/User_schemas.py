from pydantic import BaseModel

class UserSchema(BaseModel):
    full_name: str = None
    email: str
    password: str

