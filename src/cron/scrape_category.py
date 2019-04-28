from requests_html import HTMLSession
from src.modules.connector import db, category, store, product
from sqlalchemy import select


def get_calories_row(nutrients_table):
    possible_placements = [
        "//div/table/tbody/tr/td[not(text())]/following-sibling::td[contains(.,'kcal')]",
        "//div/table/tbody/tr/td[contains(.,'Energ') or contains(.,'energ')]/following-sibling::td",
        "//div/table/tbody/tr/td[contains(.,'kcal')]/following-sibling::td"
    ]
    for placement in possible_placements:
        row = nutrients_table.xpath(placement, first=True)
        if row:
            return row
    raise ValueError("Could not find calories row")


def get_calories(nutrients_info):
    calories_part = (nutrients_info.text.split("kcal")[0]).strip()
    result = ""
    for symbol in reversed(calories_part):
        if not symbol.isdigit():
            break
        result = symbol + result
    return result


def get_product_id(store_product_id, store_id):
    product_row = db.execute(select([product.c.id]).where(
        product.c.store_product_id == store_product_id).where(product.c.store == store_id)).fetchone()
    return product_row.id if product_row else None


def add_product(attrs):
    db.execute(product.insert().values(**attrs))


def update_product(product_id, attrs):
    db.execute(product.update().where(product.c.id == product_id).values(**attrs))


def scrape(store_id, store_link, category_link, category_id):
    page = 1
    page_string = "/all?page="
    category_link = store_link + "shop/" + category_link + page_string
    product_link = store_link + "products/"

    session = HTMLSession()
    while True:
        request = session.get(category_link + str(page))
        products = request.html.xpath("//a[@class='product-tile--title product-tile--browsable']")
        if not products:
            break
        for p in products:
            store_product_id = p.attrs['href'].rsplit('/', 1)[1]
            request = session.get(product_link + store_product_id)
            nutrients_div = request.html.xpath(
                "//div/h3[contains(.,'Výživové hodnoty')]/parent::*", first=True)
            if not nutrients_div:
                continue
            calories_row = get_calories_row(nutrients_div)
            calories = get_calories(calories_row)
            product_info = dict(
                store_product_id=store_product_id,
                name=p.text,
                calories=calories,
                price=1,
                unit_price=True,
                category=category_id,
                store=store_id)
            product_id = get_product_id(store_product_id, store_link)
            if product_id:
                update_product(product_id, product_info)
            else:
                add_product(product_info)
        page += 1
