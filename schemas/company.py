from pydantic import BaseModel
from typing import Optional
from typing import List

class CompanyBase(BaseModel):
    name: str
    rating: Optional[float] = None


class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True
        

