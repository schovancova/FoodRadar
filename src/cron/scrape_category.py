from requests_html import HTMLSession
from src.modules.product import ProductTesco
from src.modules.store import Tesco


def scrape(store, category):
    store = Tesco(store)
    page = 1
    html_session = HTMLSession()
    while True:
        request = html_session.get(store.get_category_link(category.link) + str(page))
        products = request.html.xpath(store.xpath["products"])
        if not products:
            break
        for p in products:
            product = ProductTesco(p)
            product_link = product.get_link(store.products_link)
            request = html_session.get(product_link)
            nutrients_div = request.html.xpath(product.xpath["nutrients_div"], first=True)
            if not nutrients_div:
                continue
            calories = product.get_calories(nutrients_div)
            price_div = request.html.xpath(product.xpath["price_div"], first=True)
            price = product.get_price(price_div)
            product_info = dict(
                name=p.text,
                calories=calories,
                price=price,
                unit_price=True,
                unit_type="kg",
                category=category.id,
                store=store.store.id)
            product.update_or_insert(**product_info)
        page += 1
