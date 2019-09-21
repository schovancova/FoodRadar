import threading

from flask import Flask, render_template, redirect

from src.modules.connector import session, Category, Product, Store
from src.modules.scraper import Scraper, stop_scraping
from src.modules.store import Tesco

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/db.db'


@app.route('/')
def layout():
    return render_template('layout.html')


@app.route('/products')
def products():
    product_rows = session.query(Product).all()
    return render_template('products.html', products=product_rows)


@app.route('/category/<category_id>', defaults={'action': None})
@app.route('/category/<category_id>/<action>')
def category(category_id, action):
    category_row = session.query(Category).get(category_id)
    if action == "delete":
        session.query(Product).filter(Product.category == category_id).delete()
        session.commit()
        return redirect("/category/"+category_id)
    elif action == "scrape":
        stop_scraping()
        thread = Scraper(target=category_row, daemon=True)
        thread.start()
        return redirect("/category/" + category_id)
    elif action == "stop":
        stop_scraping()
        return redirect("/category/" + category_id)
    product_rows = session.query(Product).filter(Product.category_id == category_id).all()
    is_scraping = any(isinstance(thread, Scraper) for thread in threading.enumerate())
    return render_template('category.html', category=category_row, products=product_rows, is_scraping=is_scraping)


@app.route('/categories')
def categories():
    stores = session.query(Store).all()
    return render_template('categories.html', stores=stores)


@app.route('/product/<product_id>')
def product(product_id):
    product_row = session.query(Product).get(product_id)
    store = Tesco(product_row.store)
    return render_template('product.html', product=product_row, store=store)


if __name__ == '__main__':
    app.run(debug=True)

