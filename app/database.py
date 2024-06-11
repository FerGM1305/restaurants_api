import pandas as pd
from .models import db, Restaurant

def import_csv_to_db(csv_file):
    data = pd.read_csv(csv_file)
    for _, row in data.iterrows():
        restaurant = Restaurant(
            id=row['id'],
            rating=row['rating'],
            name=row['name'],
            site=row['site'],
            email=row['email'],
            phone=row['phone'],
            street=row['street'],
            city=row['city'],
            state=row['state'],
            lat=row['lat'],
            lng=row['lng']
        )
        db.session.add(restaurant)
    db.session.commit()
