from pydantic import BaseModel, ConfigDict

class EmployeeBase(BaseModel):
    name: str
    position: str  # "trainer" | "admin" | "manager"
    phone: str

    model_config = ConfigDict(from_attributes=True)
class EmployeeCreate(EmployeeBase):
    pass



class Employee(EmployeeBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
