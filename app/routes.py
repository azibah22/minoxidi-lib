from flask import render_template, request, redirect, url_for
from . import app, db
from .models import Product, Category

@app.route('/')
def home():
    featured_products = Product.query.limit(4).all()
    return render_template('home.html', featured_products=featured_products)

@app.route('/products')
def products():
    search = request.args.get('search', '')
    category_id = request.args.get('category')
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if category_id:
        query = query.filter_by(category_id=category_id)
    products = query.all()
    categories = Category.query.all()
    return render_template('products.html', products=products, categories=categories)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/interested-cart')
def interested_cart():
    return render_template('interested_cart.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')
