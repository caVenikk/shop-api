from sqlalchemy import Column, ForeignKey, Integer, String, Float, func, BigInteger, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Создается базовый класс Base, который будет использоваться для определения моделей данных.
Base = declarative_base()


# Определение класса User, который представляет собой модель данных для таблицы "users".
class User(Base):
    __tablename__ = "users"

    # Определение столбцов таблицы "users" и их типов данных.
    # Здесь же определяется, является ли столбец первичным ключом, и если является, то устанавливается свойство для
    # автоматического инкремента данного поля. При описании поля также указывается, можно ли хранить в столбце
    # NULL-значения. Также можно установить значение по умолчанию, например, как в столбце active.
    id = Column("id", BigInteger, primary_key=True, autoincrement=False)
    first_name = Column("first_name", String, nullable=False)
    second_name = Column("second_name", String, nullable=True)
    username = Column("username", String, nullable=True)
    active = Column("active", Boolean, nullable=False, default=True)

    # Создается связь между таблицей "users" и таблицей "orders". Здесь указывается, что у каждого пользователя может
    # быть несколько заказов, и связь будет отслеживаться через атрибут user в модели Order.
    orders = relationship("Order", back_populates="user")


# Определение класса Product, который представляет собой модель данных для таблицы "products".
class Product(Base):
    __tablename__ = "products"

    # Определение столбцов таблицы "products" и их типов данных.
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    price = Column("price", Float, nullable=False)
    weight = Column("weight", Float, nullable=True)
    description = Column("description", String, nullable=True)
    active = Column("active", Boolean, nullable=False, default=True)

    # Создается связь между таблицей "products" и таблицей "orders". Здесь указывается, что каждый продукт может быть
    # связан с несколькими заказами, и связь будет отслеживаться через атрибут products в модели Order.
    orders = relationship("Order", secondary="orders_products", back_populates="products")


# Определение класса Order, который представляет собой модель данных для таблицы "orders".
class Order(Base):
    __tablename__ = "orders"

    # Определение столбцов таблицы "orders" и их типов данных.
    # Для столбца ordered_at определяется значение по умолчанию - текущая дата.
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    ordered_at = Column("ordered_at", DateTime(timezone=True), nullable=False, server_default=func.now())
    name = Column("name", String, nullable=False)
    phone_number = Column("phone_number", String, nullable=False)
    country_code = Column("country_code", String, nullable=False)
    state = Column("state", String, nullable=True)
    city = Column("city", String, nullable=False)
    street_line1 = Column("street_line1", String, nullable=False)
    street_line2 = Column("street_line2", String, nullable=True)
    post_code = Column("post_code", String, nullable=False)
    total_amount = Column("total_amount", Integer, nullable=False)

    # Создаются связи между таблицей "orders" и таблицами "users" и "products". Здесь указывается, что каждый заказ
    # связан с одним пользователем через атрибут user в модели User, а также может быть связан с несколькими продуктами
    # через атрибут products в модели Product.
    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary="orders_products", back_populates="orders")


# Определение класса OrderProduct, который представляет собой модель данных для таблицы "orders_products".
class OrderProduct(Base):
    __tablename__ = "orders_products"

    # Определение столбцов таблицы "orders_products" и их типов данных.
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    order_id = Column("order_id", Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column("product_id", Integer, ForeignKey("products.id"), nullable=False)
