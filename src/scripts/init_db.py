from src.modules.connector import session, Category, Store

session.query(Category).delete()
session.query(Store).delete()
session.commit()

store = Store(name="Tesco", link="https://nakup.itesco.cz/groceries/cs-CZ/")
session.add(store)

session.add_all([
    Category(name="DAIRY", full_name="Mléčné výrobky a vejce", link="mlecne-vyrobky-a-vejce", store=store.id),
    Category(name="PASTRY", full_name="Pečivo", link="pecivo", store=store.id)])
