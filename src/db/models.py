from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    func,
    Index,
    BigInteger,
    Boolean,
    DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column('id', BigInteger, primary_key=True, autoincrement=False)

    first_name = Column('first_name', String, nullable=False)
    second_name = Column('second_name', String, nullable=True)
    username = Column('username', String, nullable=True)
    active = Column('active', Boolean, nullable=False, default=True)

    orders = relationship("Order", back_populates="user")

    __table_args__ = (
        Index('user_username_index', 'username'),
        Index('user_case_insensitive_username_index', func.lower('username')),
    )


class Product(Base):
    __tablename__ = "products"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String, nullable=False)
    price = Column('price', Float, nullable=False)
    weight = Column('weight', Float, nullable=True)
    description = Column('description', String, nullable=True)
    active = Column('active', Boolean, nullable=False, default=True)

    __table_args__ = (
        Index('product_title_index', 'title'),
        Index('product_case_insensitive_title_index', func.lower('title')),
        Index('product_price_index', 'price'),
    )


class Order(Base):
    __tablename__ = "orders"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(
        'product_id',
        Integer,
        ForeignKey('products.id'),
        nullable=False
    )
    ordered_at = Column('ordered_at', DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column('name', String, nullable=False)
    phone_number = Column('phone_number', String, nullable=False)
    country_code = Column('country_code', String, nullable=False)
    state = Column('state', String, nullable=True)
    city = Column('city', String, nullable=False)
    street_line1 = Column('street_line1', String, nullable=False)
    street_line2 = Column('street_line2', String, nullable=True)
    post_code = Column('post_code', String, nullable=False)
    total_amount = Column('total_amount', Integer, nullable=False)

    user = relationship("User", back_populates="orders")
