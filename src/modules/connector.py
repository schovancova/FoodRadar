import os

from sqlalchemy import Column, Numeric, String, Integer, ForeignKey, func, create_engine, MetaData, Table, DateTime, \
    Boolean
from datetime import datetime

metadata = MetaData()

# products table
product = Table(
    'product',
    metadata,
    # internal product id
    Column('id', Integer, primary_key=True),
    # product id in store
    Column('store_product_id', Integer, nullable=False),
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
    Column('last_update', DateTime, default=datetime.utcnow, nullable=False),
    Column('created', DateTime, default=datetime.utcnow, nullable=False),
    Column('store', ForeignKey('store.id'), nullable=False),
)

# product categories
category = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True),
    # keyword name
    Column('name', String(64), nullable=False),
    Column('link', String(64), nullable=False),
    # name as seen on website
    Column('full_name', String(64), nullable=False),
    Column('store', ForeignKey('store.id'), nullable=False),
    Column('category', ForeignKey('category.id'), nullable=True),
)

# stores with products
store = Table(
    'store',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64), nullable=False),
    Column('link', String(64), nullable=False),
)

project_root = os.path.dirname(os.path.dirname(__file__))
output_path = os.path.join(project_root, 'db/db.db')
engine = create_engine('sqlite:///' + output_path)
metadata.create_all(engine)
db = engine.connect()
