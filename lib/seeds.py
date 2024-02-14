from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review

# Connect to the database
engine = create_engine('sqlite:///db/restaurants.db')
Base.metadata.bind = engine

# Create a session to interact with the database
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Seed data for restaurants
restaurant1 = Restaurant(name='Restaurant A', price=3)
restaurant2 = Restaurant(name='Restaurant B', price=4)
restaurant3 = Restaurant(name='Restaurant C', price=5)

session.add_all([restaurant1, restaurant2, restaurant3])
session.commit()

# Seed data for customers
customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')
customer3 = Customer(first_name='Alice', last_name='Johnson')

session.add_all([customer1, customer2, customer3])
session.commit()

# Seed data for reviews
review1 = Review(star_rating=4, restaurant=restaurant1, customer=customer1)
review2 = Review(star_rating=5, restaurant=restaurant2, customer=customer2)
review3 = Review(star_rating=3, restaurant=restaurant3, customer=customer3)

session.add_all([review1, review2, review3])
session.commit()

# Close the session
session.close()