from src.modules.connector import session, Category, Store

session.query(Category).delete()
session.query(Store).delete()

store = Store(name="Tesco", link="https://nakup.itesco.cz/groceries/cs-CZ/")
session.add(store)
session.commit()

session.add_all([
    Category(name="DAIRY", full_name="Mléčné výrobky a vejce", link="mlecne-vyrobky-a-vejce", store_id=store.id),
    Category(name="PASTRY", full_name="Pečivo", link="pecivo", store_id=store.id),
    Category(name="MEAT", full_name="Maso, ryby a lahůdky", link="maso-ryby-a-lahudky", store_id=store.id),
    Category(name="DURABLE", full_name="Trvanlivé potraviny", link="trvanlive-potraviny", store_id=store.id),
    Category(name="FROZEN", full_name="Mražené potraviny", link="mrazene-potraviny", store_id=store.id),
    Category(name="DRINKS", full_name="Nápoje", link="napoje", store_id=store.id),
    Category(name="ALCOHOL", full_name="Alkoholické nápoje", link="alkoholicke-napoje", store_id=store.id),
    Category(name="HOUSEHOLD", full_name="Péče o domácnost", link="pece-o-domacnost", store_id=store.id),
    Category(name="DRUGSTORE", full_name="Drogerie a kosmetika", link="drogerie-a-kosmetika", store_id=store.id),
    Category(name="KIDS", full_name="Péče o děti", link="pece-o-deti", store_id=store.id),
    Category(name="HOME", full_name="Domov a zábava", link="domov-a-zabava", store_id=store.id),
    Category(name="PETS", full_name="Chovatelské potřeby", link="chovatelske-potreby", store_id=store.id)])

session.commit()
