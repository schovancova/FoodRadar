from src.modules.connector import db, category, store
from sqlalchemy import select
from src.cron.scrape_category import scrape


# TODO change to fetchall when more stores come up
actual_store = db.execute(select([store.c.id, store.c.link])).fetchone()
categories = db.execute(
    select([category.c.link, category.c.id]).where(category.c.store == actual_store.id)).fetchall()

for category in categories:
    scrape(actual_store.id, actual_store.link, category.link, category.id)
