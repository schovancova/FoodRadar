from src.modules.connector import db, category, store

db.execute(category.delete())
db.execute(store.delete())

store_id = db.execute(store.insert().values([
    {"name": "Tesco", "link": "https://nakup.itesco.cz/groceries/cs-CZ/"},
])).lastrowid

db.execute(category.insert().values([
    {"name": "DAIRY", "full_name": "Mléčné výrobky a vejce", "link": "mlecne-vyrobky-a-vejce", "store": store_id},
    {"name": "PASTRY", "full_name": "Pečivo", "link": "pecivo", "store": store_id},
]))
