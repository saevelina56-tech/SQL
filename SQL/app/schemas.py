from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from decimal import Decimal

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    
    class Config:
        from_attributes = True



class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int
    
    class Config:
        from_attributes = True



class UserBase(BaseModel):
    name: str
    email: str
    role_id: int

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True



class ClientBase(BaseModel):
    name: str
    phone: str

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    
    class Config:
        from_attributes = True



class CarBase(BaseModel):
    brand: str
    model: str
    year: int
    client_id: int

class CarCreate(CarBase):
    pass

class CarResponse(CarBase):
    id: int
    
    class Config:
        from_attributes = True



class ServiceBase(BaseModel):
    name: str
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    
    class Config:
        from_attributes = True



class OrderItem(BaseModel):
    service_id: int
    quantity: int = Field(ge=1, default=1)

class OrderBase(BaseModel):
    client_id: int
    car_id: int
    user_id: int

class OrderCreate(OrderBase):
    services: List[OrderItem]

class OrderResponse(BaseModel):
    id: int
    client_id: int
    car_id: int
    user_id: int
    created_at: datetime
    status: str
    services: List[ServiceResponse]
    
    class Config:
        from_attributes = True

class OrderUpdateStatus(BaseModel):
    status: str