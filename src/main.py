from requests_html import HTMLSession
import src.modules.connector as db


def get_calories_row(nutrients_table):
    possible_placements = [
        "//div/h3[contains(.,'Výživové hodnoty')]/parent::*",
        "//div/table/tbody/tr/td[contains(.,'Energ') or contains(.,'energ')]/following-sibling::td[contains(.,'/')]",
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


def add_to_products(name, link, calories):
    print(name)
    print(calories)
    product_data.append({
        "name": name,
        "link": link,
        "kcal": calories
    })


BASE_URL = "https://nakup.itesco.cz/"
URL = f"{BASE_URL}/groceries/cs-CZ/shop/mlecne-vyrobky-a-vejce/all"
page = 1
page_string = "?page="

product_data = []

session = HTMLSession()

while False:
    request = session.get(URL + page_string + str(page))
    products = request.html.xpath("//a[@class='product-tile--title product-tile--browsable']")
    if not products:
        break
    for product in products:
        request = session.get(BASE_URL + product.attrs['href'])
        nutrients_div = request.html.xpath(
            "//div/h3[contains(.,'Výživové hodnoty')]/parent::*", first=True)
        if not nutrients_div:
            continue
        calories_row = get_calories_row(nutrients_div)
        calories = get_calories(calories_row)
        add_to_products(name=product.text, link=product.attrs['href'], calories=calories)
    page += 1

for c in db.product.c:
    print(c)
