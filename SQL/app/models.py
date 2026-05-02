from sqlalchemy import(
    Table, Column, String, Integer, Float, Numeric, Text, DateTime, Date,
    Boolean, ForeignKey, Index, CheckConstraint, UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    
    orders = relationship("Order", back_populates="client") 
    cars = relationship("Car", back_populates="client")

class Car(Base):
    __tablename__ = 'cars'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id'))
    
    client = relationship("Client", back_populates="cars")
    orders = relationship("Order", back_populates="car")

client_cars = Table(
    "client_cars", Base.metadata,
    Column('client_id', Integer, ForeignKey('clients.id', ondelete='cascade'), primary_key=True),
    Column('car_id', Integer, ForeignKey('cars.id', ondelete='cascade'), primary_key=True),
)

class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    
    orders = relationship("Order", secondary='order_services', back_populates="services")

order_services = Table(
    "order_services", Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id', ondelete='cascade'), primary_key=True),
    Column('service_id', Integer, ForeignKey('services.id', ondelete='cascade'), primary_key=True),
    Column('quantity', Integer, default=1)
)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), nullable=False)
    
    client = relationship("Client", back_populates="orders")
    car = relationship("Car", back_populates="orders")
    services = relationship("Service", secondary=order_services, back_populates="orders")
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    
    role = relationship("Role", back_populates="users")
    orders = relationship("Order", back_populates="user")
    
class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    
    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", secondary='role_permissions', back_populates="roles")

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)


class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    roles = relationship("Role", secondary='role_permissions', back_populates="permissions")