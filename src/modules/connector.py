import os

from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, create_engine, DateTime, Boolean
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    store_product_id = Column(Integer, nullable=False)
    category = Column(ForeignKey('category.id'), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    is_discount = Column(Boolean, nullable=False, default=True)
    # price during discount
    discount_price = Column(Numeric, nullable=True)
    # price per unit
    unit_price = Column(Numeric, nullable=False)
    # type of unit (kg/l/..)
    unit_type = Column(String, nullable=False)
    weight = Column(Numeric, nullable=True)
    calories = Column(Numeric, nullable=True)
    fats = Column(Numeric, nullable=True)
    carbohydrates = Column(Numeric, nullable=True)
    sugars = Column(Numeric, nullable=True)
    protein = Column(Numeric, nullable=True)
    salt = Column(Numeric, nullable=True)
    last_update = Column(DateTime, default=datetime.utcnow, nullable=False)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    store = Column(ForeignKey('store.id'), nullable=False)


# product categories
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    # keyword name
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    # name as seen on website
    full_name = Column(String, nullable=False)
    store = Column(ForeignKey('store.id'), nullable=False)
    category = Column(ForeignKey('category.id'), nullable=True)


# stores with products
class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)


project_root = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(project_root, 'db/db.db')
engine = create_engine('sqlite:///' + output_path)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
