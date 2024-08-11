from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    unique_id = Column(Integer, index=True)
    username = Column(String(256), index=True)
    balance = Column(Float)
    telephone_number = Column(String(256))
    passport_image = Column(String(256))
    region = Column(String(256))
    address = Column(String(256))
    password = Column(String(256))
    email = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
    first_name = Column(String(256))
    last_name = Column(String(256))
    is_verified = Column(Boolean, default=False)
    product = relationship('Products', back_populates='user')
    order = relationship('Orders', back_populates='user')
    notification = relationship('Notifications', back_populates='user')

    def __repr__(self):
        return f"<User(Id={self.id}, username={self.username})>"


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, unique=True, index=True)
    tracking_code = Column(String(256), unique=True, index=True)
    quantity = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    flight = Column(Integer, index=True)
    product_title = Column(String(256), index=True)
    user = relationship('Users', back_populates='product')
    order = relationship('Orders', back_populates='product')

    def __repr__(self):
        return f"<Product(Id={self.id}, product_title={self.product_title} ,tracking_code={self.tracking_code}, flight={self.flight})>"


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, unique=True, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, default='collecting')
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship('Products', back_populates='order')
    user = relationship('Users', back_populates='order')

    def __repr__(self):
        return f"<Order(Id={self.id}, product={self.product_id}, status={self.status})>"


class Notifications(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String(256))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    user = relationship('Users', back_populates='notification')

    def __repr__(self):
        return f"<Notification(Id={self.id}, is_read={self.is_read})>"




