from requests_html import HTMLSession
from src.modules.connector import session, Product, Store, Category


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
    product_row = session.query(Product.id).filter(
        Product.store_product_id == store_product_id).filter(Product.store == store_id).first()
    return product_row.id if product_row else None


def add_product(attrs):
    product = Product(**attrs)
    session.add(product)


def update_product(product_id, attrs):
    session.query(Product).filter_by(id=product_id).update(**attrs)
    session.commit()


def scrape(store, category):
    page = 1
    page_string = "/all?page="
    category_link = store.link + "shop/" + category.link + page_string
    product_link = store.link + "products/"

    html_session = HTMLSession()
    while True:
        request = html_session.get(category_link + str(page))
        products = request.html.xpath("//a[@class='product-tile--title product-tile--browsable']")
        if not products:
            break
        for p in products:
            store_product_id = p.attrs['href'].rsplit('/', 1)[1]
            request = html_session.get(product_link + store_product_id)
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
                category=category.id,
                store=store.id)
            product_id = get_product_id(store_product_id, store.link)
            if product_id:
                update_product(product_id, product_info)
            else:
                add_product(product_info)
        page += 1
