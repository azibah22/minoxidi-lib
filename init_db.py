from app import app, db
from app.models import Category, Product, User

with app.app_context():
    # Create all tables
    db.create_all()

    # Add sample categories
    cat1 = Category.query.filter_by(name='Hair Growth').first() or Category(name='Hair Growth')
    cat2 = Category.query.filter_by(name='Beard Growth').first() or Category(name='Beard Growth')
    if not cat1.id:
        db.session.add(cat1)
    if not cat2.id:
        db.session.add(cat2)
    db.session.commit()

    # Add sample products
    if not Product.query.first():
        prod1 = Product(name='Minoxidil 5% Solution', description='Effective for hair regrowth.', price=25.0, image_url='/static/placeholder.png', category_id=cat1.id)
        prod2 = Product(name='Minoxidil Foam', description='Easy to apply foam for scalp.', price=30.0, image_url='/static/placeholder.png', category_id=cat1.id)
        prod3 = Product(name='Minoxidil Beard Booster', description='Specially formulated for beard growth.', price=28.0, image_url='/static/placeholder.png', category_id=cat2.id)
        db.session.add_all([prod1, prod2, prod3])
        db.session.commit()

    # Add default admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Default admin user created: admin / admin123')

    print('Database initialized with sample data.') 