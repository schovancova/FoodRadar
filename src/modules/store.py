
class Tesco:
    def __init__(self, store):
        self.store = store
        self.page_picker = "/all?page="
        self.xpath = {
            "products": "//a[@data-auto='product-tile--title']",
        }

    def get_category_link(self, category_path):
        return self.store_link + category_path + self.page_picker

    @property
    def store_link(self):
        return self.store.link + "shop/"

    @property
    def products_link(self):
        return self.store.link + "products/"
