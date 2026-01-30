from pydantic import BaseModel, EmailStr
from typing import Optional

class OnboardingState(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = "salesman"
    team_id: Optional[int] = None

    def is_complete(self) -> bool:
        return all([
            self.name,
            self.email,
            self.password,
            self.role
        ])
