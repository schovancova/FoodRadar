from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, func, create_engine, MetaData, Table, DateTime, \
    Boolean
from sqlalchemy.orm import sessionmaker
from datetime import datetime

timestamp = datetime.utcnow()
metadata = MetaData()

product = Table(
    'product',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('category', ForeignKey('category.id'), nullable=False),
    Column('name', String(64), nullable=False),
    Column('price', Numeric, nullable=False),
    Column('is_discount', Boolean, nullable=False, default=True),
    # price during discount
    Column('discount_price', Numeric, nullable=True),
    # is the price per unit or per kg
    Column('unit_price', Boolean, nullable=False),
    Column('weight', Numeric, nullable=True),
    Column('calories', Numeric, nullable=True),
    Column('fats', Numeric, nullable=True),
    Column('carbohydrates', Numeric, nullable=True),
    Column('sugars', Numeric, nullable=True),
    Column('protein', Numeric, nullable=True),
    Column('salt', Numeric, nullable=True),
    Column('last_update', DateTime, default=timestamp, nullable=False),
    Column('created', DateTime, default=timestamp, nullable=False),
)

category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True),
    # keyword name
    Column('name', String(64), nullable=False),
    # name as seen on website
    Column('full_name', String(64), nullable=False),
    Column('category', ForeignKey('category.id'), nullable=True),
)

engine = create_engine('sqlite:///./db/db.db')
session = sessionmaker()
session.configure(bind=engine)
metadata.create_all(engine)
