from pydantic import BaseModel 
from app.models.employee import EmployeeRole
from typing import Optional
from datetime import date,datetime




class EmployeeCreate(BaseModel):  
    employee_code: str  
    full_name: str 
    email:Optional[str] = None  
    phone:Optional[str] = None
    role: EmployeeRole 
    project_id: Optional[int] = None
    hire_date: date









class EmployeeResponse(BaseModel): 
    employee_code: str  
    full_name: str 
    email:Optional[str] = None  
    phone:Optional[str] = None
    role: EmployeeRole 
    project_id: Optional[int] = None
    hire_date: date
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}






class EmployeeUpdate(BaseModel):
    employee_code: str | None = None 
    full_name: str | None = None
    email:str | None = None  
    phone:str | None = None
    role: EmployeeRole | None = None
    project_id: int | None = None
    hire_date: date | None = None