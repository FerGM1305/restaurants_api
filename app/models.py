from . import db
from sqlalchemy.orm import validates
import validators

class Restaurant(db.Model):
    id = db.Column(db.Text, primary_key=True)
    rating = db.Column(db.Integer)
    name = db.Column(db.String)
    site = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    street = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 0 or rating > 4:
            raise ValueError("Rating must be between 0 and 4")
        return rating
    
    @validates('site')
    def validate_site(self, key, site):
        if site and not validators.url(site):
            raise ValueError("Invalid URL")
        return site
    
    
    def serialize(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'name': self.name,
            'site': self.site,
            'email': self.email,
            'phone': self.phone,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'lat': self.lat,
            'lng': self.lng
        }