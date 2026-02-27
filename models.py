from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Date, String, DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100))
    profile_picture = db.Column(db.String(200), default='default.jpg')
    # ✅ ADD THIS
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'

    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    profile_image = db.Column(db.String(200), default='default.png')
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    bookings = db.relationship('Booking', back_populates='user')

class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), default='History')
    rating = db.Column(db.Float, default=4.5)
    location = db.Column(db.String(100), default='Nepal')
    image = db.Column(db.String(255))

    bookings = db.relationship('Booking', back_populates='destination')


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    travel_date = db.Column(db.Date, nullable=False)  # ✅ Make sure this exists
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'cancelled'
    created_at = db.Column(db.DateTime, 
    default=datetime.utcnow)
 # Relationships

    user = db.relationship('User', back_populates='bookings')
    destination = db.relationship('Destination', back_populates='bookings')

