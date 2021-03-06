"""Product representation on the site"""
from src.modules.connector import Product


class ProductTesco:
    def __init__(self, session, store_id, product_html):
        self.session = session
        self.store_id = store_id
        self.product_html = product_html
        self.xpath = {
            "nutrients_div": "//div/h3[contains(.,'Výživové hodnoty')]/parent::*",
            "price_div": "//span[@data-auto='price-value']"
        }

    @property
    def product_id(self):
        return self.product_html.attrs['href'].rsplit('/', 1)[1]

    def get_link(self, products_link):
        return products_link + self.product_id

    @staticmethod
    def get_calories(nutrients_div):
        possible_placements = [
            "//div/table/tbody/tr/td[not(text())]/following-sibling::td[contains(.,'kcal')]",
            "//div/table/tbody/tr/td[contains(.,'Energ') or contains(.,'energ') or contains(.,'Výživová')]/following-sibling::td",
            "//div/table/tbody/tr/td[contains(.,'kcal')]/following-sibling::td"
        ]
        for placement in possible_placements:
            row = nutrients_div.xpath(placement, first=True)
            if row:
                break
        if not row:
            return None
        if "kcal" in row.text:
            calories_part = (row.text.split("kcal")[0]).strip()
        elif "kJ" in row.text:
            calories_part = (row.text.split("kJ")[0]).strip()
        else:
            return None
        result = ""
        for symbol in reversed(calories_part):
            if not symbol.isdigit():
                break
            result = symbol + result
        return result

    @staticmethod
    def get_price(price_div):
        return float(price_div.text.replace(",", "."))

    def update_or_insert(self, **kwargs):
        product_row = self.session.query(Product.id).filter(
            Product.store_product_id == self.product_id).filter(Product.store_id == self.store_id)
        if product_row.first():
            product_row.update(kwargs)
        else:
            product = Product(**kwargs)
            self.session.add(product)
        self.session.commit()
