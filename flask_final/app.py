from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
# from flask_migrate import Migrate



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app1.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Your secret key"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# migrate = Migrate(app, db)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")
    orders = db.relationship('Order', backref='user', lazy=True)  # Keep backref here in User model

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False)
    product = db.relationship('Product', backref=db.backref('orders', lazy=True, passive_deletes=True)) 
    quantity = db.Column(db.Integer, nullable=False, default=1)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default="Pending")  

    def __repr__(self):
        return f'<Order {self.id}>'



   

class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()

    if not User.query.filter_by(role="admin").first():
        admin_user = User(name="Admin", email="admin@gmail.com", role="admin")
        admin_user.set_password("admin123")  # Set a default password
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created with email: admin@gmail.com and password: admin123")


# Home Route
@app.route("/")
def home():
    return render_template("dashboard.html")

# Index Route
@app.route("/index")
@login_required
def index():
    return render_template("index.html")

# Profile Route
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

# Display Products Route (for users and admin)
@app.route("/displayproduct")
@login_required
def display():
    products = Product.query.all()  # Show all products
    return render_template("displayproduct.html", products=products)

# Admin: Add Product Route
@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        image_url = request.form.get("image_url")
        
        new_product = Product(
            name=name, 
            description=description, 
            price=price, 
            image_url=image_url
        )
        db.session.add(new_product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("display"))

    return render_template("add_product.html")

# User: Add Product to Cart Route
@app.route("/add_to_cart/<int:product_id>", methods=["GET", "POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    existing_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if existing_item:
        # If the product is already in the cart, increase the quantity
        existing_item.quantity += 1
    else:
        # Add the product to the cart
        new_cart_item = Cart(
            name=product.name,
            price=product.price,
            quantity=1,
            user_id=current_user.id,
            product_id=product.id
        )
        db.session.add(new_cart_item)

    db.session.commit()
    flash(f"{product.name} added to your cart!", "success")
    return redirect(url_for("cart"))  # Redirect to cart page after adding the item


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        user = User.query.filter_by(email=email, role=role).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

# Display Product Details Route
@app.route("/product")
@login_required
def product():
    products = Product.query.all()
    return render_template("product.html", products=products)


# Admin: Update Product Route
@app.route("/update_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def update_product(product_id):
    if current_user.role != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("index"))

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form.get("name")
        product.description = request.form.get("description")
        product.price = request.form.get("price")
        product.image_url = request.form.get("image_url")

        db.session.commit()

        flash("Product updated successfully!", "success")
        return redirect(url_for("display"))

    return render_template("update_product.html", product=product)

# Admin: Delete Product Route
@app.route("/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    if current_user.role != "admin":
        flash("You are not authorized to perform this action.", "danger")
        return redirect(url_for("index"))

    product = Product.query.get_or_404(product_id)

    # Remove all orders related to this product
    Order.query.filter_by(product_id=product_id).delete()

    # Now delete the product
    db.session.delete(product)
    db.session.commit()

    flash("Product deleted successfully!", "success")
    return redirect(url_for("display"))


@app.route("/cart")
@login_required
def cart():
    # Get all the cart items for the current user
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template("cart.html", cart_items=cart_items)


@app.route("/update_quantity/<int:cart_item_id>/<action>", methods=["POST"])
@login_required
def update_quantity(cart_item_id, action):
    cart_item = Cart.query.get_or_404(cart_item_id)

    # Check if the cart item belongs to the current user
    if cart_item.user_id != current_user.id:
        flash("You are not authorized to update this item.", "danger")
        return redirect(url_for("cart"))

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1
    db.session.commit()

    flash("Cart updated successfully!", "success")
    return redirect(url_for("cart"))

@app.route("/remove_from_cart/<int:cart_item_id>", methods=["POST"])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = Cart.query.get_or_404(cart_item_id)

    # Check if the cart item belongs to the current user
    if cart_item.user_id != current_user.id:
        flash("You are not authorized to remove this item.", "danger")
        return redirect(url_for("cart"))

    db.session.delete(cart_item)
    db.session.commit()

    flash("Product removed from cart.", "success")
    return redirect(url_for("cart"))

@app.route("/place_order", methods=["POST"])
@login_required
def place_order():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Your cart is empty. Cannot place an order.", "danger")
        return redirect(url_for("cart"))

    for item in cart_items:
        new_order = Order(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.session.add(new_order)
    
    # Remove items from the cart after placing the order
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    flash("Your order has been placed successfully!", "success")
    return redirect(url_for("order_confirmation"))

@app.route("/order_confirmation")
@login_required
def order_confirmation():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("order_confirmation.html", orders=orders)

@app.route("/admin/orders")
@login_required
def admin_orders():
    if current_user.role != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("index"))

    orders = Order.query.all()
    return render_template("admin_orders.html", orders=orders)

@app.route('/change_order_status/<int:order_id>', methods=['POST'])
@login_required
def change_order_status(order_id):
    if current_user.role != "admin":
        flash("You are not authorized to perform this action.", "danger")
        return redirect(url_for("admin_orders"))

    new_status = request.form['status']

    # Fetch the order and update the status
    order = Order.query.get_or_404(order_id)
    if order:
        order.status = new_status
        db.session.commit()

    flash("Order status updated successfully!", "success")
    return redirect(url_for('admin_orders'))



# Define Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    order_id = db.Column(db.String(50))
    shopping_experience = db.Column(db.String(50))
    product_quality = db.Column(db.String(50))
    liked_aspects = db.Column(db.String(250))
    purchase_frequency = db.Column(db.String(50))
    recommendation = db.Column(db.String(50))
    suggestion = db.Column(db.Text)

@app.route('/api/feedback', methods=['POST'])
def receive_feedback():
    data = request.form
    for key in data:
        print(f"  {key}: {data.getlist(key) if key == 'liked_aspects' else data.get(key)}")

    try:
        feedback = Feedback(
            name=data.get('name'),
            email=data.get('email'),
            order_id=data.get('order_id'),
            shopping_experience=data.get('shopping_experience'),
            product_quality=data.get('product_quality'),
            liked_aspects=','.join(data.getlist('liked_aspects')),
            purchase_frequency=data.get('purchase_frequency'),
            recommendation=data.get('recommendation'),
            suggestion=data.get('suggestion')
        )
        db.session.add(feedback)
        db.session.commit()
        return "Feedback received successfully", 200
    except Exception as e:
        return "Failed to save feedback", 500




@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    feedbacks = Feedback.query.all()
    feedback_list = []
    for fb in feedbacks:
        feedback_list.append({
            'name': fb.name,
            'email': fb.email,
            'order_id': fb.order_id,
            'shopping_experience': fb.shopping_experience,
            'product_quality': fb.product_quality,
            'liked_aspects': fb.liked_aspects,
            'purchase_frequency': fb.purchase_frequency,
            'recommendation': fb.recommendation,
            'suggestion': fb.suggestion
        })
    return jsonify(feedback_list)



@app.route('/api/about-us', methods=['GET'])
def about_us_api():
    rendered_html = render_template('about.html')
    return rendered_html  # This returns raw HTML as a response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("🔧 Database tables created.")
    app.run(debug=True)



