from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Destination, Booking
from config import Config
from functools import wraps
from datetime import datetime
from flask_migrate import Migrate  
from werkzeug.utils import secure_filename
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate                              
    # DECORATORS FIRST
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first!')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or session.get('role') != 'admin':
                flash('Admin access required!')
                abort(403)
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/')
    def home():
        destinations = Destination.query.limit(6).all()
        return render_template('home.html', destinations=destinations)

    @app.route('/destinations')
    def destinations():
        search = request.args.get('search', '')
        category = request.args.get('category', 'All')
        query = Destination.query
        
        if search:
            query = query.filter(
                Destination.name.contains(search) | 
                Destination.description.contains(search)
            )
        if category != 'All':
            query = query.filter_by(category=category)
            
        return render_template('destinations.html', destinations=query.all())

    # ✅ FIXED: ADD THIS MISSING ROUTE
    @app.route('/packages')
    def packages():
        destinations = Destination.query.all()
        return render_template('packages.html', destinations=destinations)

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['email']).first()
            if user and user.check_password(request.form['password']):
                session.update({
                    'user_id': user.id, 
                    'username': user.username, 
                    'role': user.role
                })
                flash('Welcome back!')
                return redirect(url_for('home'))
            flash('Invalid credentials!')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            if User.query.filter_by(email=request.form['email']).first():
                flash('Email already registered!')
                return render_template('register.html')
            user = User(
                username=request.form['username'],
                email=request.form['email']
            )
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged out successfully!')
        return redirect(url_for('home'))

    @app.route('/book/<int:dest_id>', methods=['GET', 'POST'])
    @login_required
    def book(dest_id):
        destination = Destination.query.get_or_404(dest_id)
        user_id = session['user_id']
        
        if request.method == 'POST':
            travel_date_str = request.form.get('travel_date')  # e.g., "2026-03-23"
            payment_method = request.form.get('payment_method')  # e.g., 'credit_card', 'paypal'

            if not travel_date_str:
                flash("Please select a travel date!")
                return redirect(url_for('book', dest_id=dest_id))

            # ✅ Convert string to Python date object
            travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d").date()

            # ✅ Create the booking
            booking = Booking(
                user_id=user_id,
                destination_id=dest_id,
                travel_date=travel_date,
                status='pending'
            )

            db.session.add(booking)
            db.session.commit()  # Save the booking to the database

            # Simulate payment
            payment_success = True
            if payment_success:
                booking.status = 'confirmed'
                db.session.commit()
                flash(f'Booking confirmed for {destination.name}! 🎉')
            else:
                flash('Payment failed. Please try again.')

            return redirect(url_for('dashboard'))

        return render_template('book.html', destination=destination)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user = User.query.get(session['user_id'])
        bookings = Booking.query.filter_by(user_id=session['user_id']).all()
        return render_template('dashboard.html', bookings=bookings, user=user)

    @app.route('/admin/users')
    @admin_required
    def admin_users():
        users = User.query.all()
        return render_template('admin/users.html', users=users)
    
    @app.route('/admin/bookings')
    @admin_required
    def admin_bookings():
        status_filter = request.args.get('status', 'all')  # pending, confirmed, all
        query = Booking.query

        if status_filter in ['pending', 'confirmed']:
            query = query.filter_by(status=status_filter)

        bookings = query.order_by(Booking.date_created.desc()).all()
        return render_template('admin/bookings.html', bookings=bookings, status_filter=status_filter)
    
    @app.route('/admin/bookings/confirm/<int:booking_id>', methods=['POST'])
    @admin_required
    def admin_confirm_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        if booking.status == 'pending':
            booking.status = 'confirmed'
            db.session.commit()
            flash(f'Booking ID {booking.id} confirmed successfully! 🎉')
        else:
            flash(f'Booking ID {booking.id} is already confirmed.')
        return redirect(url_for('admin_bookings'))
    
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        user = User.query.get(session.get('user_id'))
        if not user:
            flash("User not found. Please login again.", "danger")
            session.clear()
            return redirect(url_for('login'))
        if request.method == 'POST':
            username = request.form.get('username')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            
            user.username = username
            user.full_name = full_name
            user.phone = phone
            user.address = address
            
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('profile'))
        return render_template('profile.html', user=user)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
