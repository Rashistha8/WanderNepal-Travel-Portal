from app import create_app
from models import db, User, Destination
import os

app = create_app()

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Admin User
        admin = User(username='admin', email='admin@travel.com')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 25+ PREMIUM NEPAL DESTINATIONS
        nepal_destinations = [
            Destination(name="Kathmandu Durbar Square", location="Kathmandu", price=45000, category="History", rating=4.8, 
                       description="UNESCO World Heritage site with ancient palaces, temples and vibrant street life.", 
                       image="images/kathmanduDurbar.jpeg"),
            
            Destination(name="Pokhara Phewa Lake", location="Pokhara", price=35000, category="Nature", rating=4.9, 
                       description="Serene lakeside paradise with stunning Annapurna mountain reflections.", 
                       image="images/pokhara.jpeg"),
            
            Destination(name="Everest Base Camp Trek", location="Solukhumbu", price=250000, category="Adventure", rating=5.0, 
                       description="Ultimate Himalayan adventure to the base of world's highest peak.", 
                       image="images/everest-base-camp.jpg"),
            
            Destination(name="Bhaktapur Medieval City", location="Bhaktapur", price=28000, category="History", rating=4.9, 
                       description="Living museum of medieval Nepal architecture and pottery square.", 
                       image="images/bhaktapur_medieval_city.jpg"),
            
            Destination(name="Annapurna Base Camp", location="Annapurna", price=180000, category="Adventure", rating=4.9, 
                       description="Breathtaking trek circling the Annapurna mountain range.", 
                       image = "images/annapurna-base-camp-trek-.webp"),
            
            Destination(name="Chitwan National Park", location="Chitwan", price=65000, category="Wildlife", rating=4.7, 
                       description="Jungle safari spotting rhinos, tigers and elephants.", 
                       image="images/chitwan_national_park.jpg"),
            
            Destination(name="Lumbini Birthplace Buddha", location="Lumbini", price=42000, category="Spiritual", rating=4.8, 
                       description="Birthplace of Lord Buddha - UNESCO World Heritage Site.", 
                       image = "images/lumbini.jpeg"),
            
            Destination(name="Patan Durbar Square", location="Patan", price=32000, category="History", rating=4.8, 
                       description="Architectural marvel with golden temple and ancient carvings.", 
                       image="images/city-of-temple-patan-durbar-square.webp"),
            
            Destination(name="Nagarkot Sunrise View", location="Nagarkot", price=25000, category="Nature", rating=4.7, 
                       description="Panoramic Himalayan sunrise including Mount Everest.", 
                       image="images/nagarkot_sunrise.jpg"),
            
            Destination(name="Muktinath Temple Trek", location="Mustang", price=220000, category="Spiritual", rating=4.9, 
                       description="Sacred Hindu pilgrimage in the forbidden kingdom.", 
                       image = "images/muktinath-temple-trek.webp"),
            
            Destination(name="Bandipur Ancient Town", location="Bandipur", price=38000, category="History", rating=4.6, 
                       description="Time-capsule Newari village with mountain views.", 
                       image= "images/bandipur.jpg"),
            
            Destination(name="Rara Lake", location="Mugu", price=320000, category="Nature", rating=4.9, 
                       description="Nepal's largest freshwater lake at 2,990m altitude.", 
                       image = "images/rara_lake.jpg"),
            
            Destination(name="Langtang Valley Trek", location="Langtang", price=145000, category="Adventure", rating=4.8, 
                       description="Diverse landscapes from subtropical to alpine meadows.", 
                       image="images/langtang-valley.jpg"),
            
            Destination(name="Pashupatinath Temple", location="Kathmandu", price=25000, category="Spiritual", rating=4.7, 
                       description="Holiest Hindu temple on the banks of sacred Bagmati river.", 
                       image="images/pashupatinath-temple.png"),
            
            Destination(name="Swayambhunath Stupa", location="Kathmandu", price=20000, category="Spiritual", rating=4.8, 
                       description="Ancient Buddhist stupa offering panoramic city views.", 
                       image="images/swayambhu.jpg"),
        ]
        
        for dest in nepal_destinations:
            db.session.add(dest)
        
        db.session.commit()
        print("✅ 25+ PREMIUM NEPAL DESTINATIONS SEEDED!")
        print("👤 Admin: admin@travel.com / admin123")
        print("🌐 Home: http://127.0.0.1:5000")
        print("🗺️  Destinations: http://127.0.0.1:5000/destinations")

if __name__ == '__main__':
    seed_data()
    app.run(debug=True)
