from pydantic import BaseModel

class EmployeeBase(BaseModel):
    name: str
    position: str  # "trainer" | "admin" | "manager"
    phone: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: str

    class Config:
        from_attributes = True
