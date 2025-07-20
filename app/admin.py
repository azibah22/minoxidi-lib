from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from . import app, db
from .models import Product, Category, User

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
@login_required
def admin_dashboard():
    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        image_file = request.files.get('image_file')
        image_url = ''
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            image_file.save(os.path.join(UPLOAD_FOLDER, filename))
            image_url = f'uploads/{filename}'
        product = Product(name=name, description=description, price=price, image_url=image_url, category_id=category_id)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.category_id = int(request.form['category_id'])
        image_file = request.files.get('image_file')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            image_file.save(os.path.join(UPLOAD_FOLDER, filename))
            product.image_url = f'uploads/{filename}'
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/users')
@login_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.')
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('User added successfully!')
            return redirect(url_for('manage_users'))
    return render_template('admin/add_user.html')

@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        password = request.form['password']
        if password:
            if len(password) < 6:
                flash('Password must be at least 6 characters.')
            else:
                user.set_password(password)
                db.session.commit()
                flash('Password updated!')
                return redirect(url_for('manage_users'))
    return render_template('admin/edit_user.html', user=user)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account while logged in.')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!')
    return redirect(url_for('manage_users'))

@app.route('/admin/categories')
@login_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        if Category.query.filter_by(name=name).first():
            flash('Category already exists.')
        else:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully!')
            return redirect(url_for('manage_categories'))
    return render_template('admin/add_category.html')

@app.route('/admin/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == 'POST':
        name = request.form['name']
        if Category.query.filter(Category.name == name, Category.id != category_id).first():
            flash('Another category with this name already exists.')
        else:
            category.name = name
            db.session.commit()
            flash('Category updated!')
            return redirect(url_for('manage_categories'))
    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.products:
        flash('Cannot delete a category with products.')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!')
    return redirect(url_for('manage_categories'))
