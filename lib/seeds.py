from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Review, Restaurant, Customer
import ipdb

fake = Faker()

if __name__ == "__main__":
    engine = create_engine("sqlite:///db/restaurant.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    # session.query(Review).delete() #clear table
    print("before")

    
    cust = session.get(Customer, 2)
    rest = session.get(Restaurant,2)
    rest2 = session.get(Restaurant, 4)
    rev = session.get(Review, 2)
    ipdb.set_trace()
    
    
    customer = [Customer(
        first_name= fake.first_name(),
        last_name= fake.last_name()
    ) for _ in range(50)]

    restaurant = [Restaurant(
        name= fake.name(),
        price = random.randint(100, 3500)
    ) for _ in range(50)]


    review = []
    for i in range(50):
        review1 = Review(
        star_rating = random.randint(1,6),
        comment = fake.sentence(),
        customer_id = i,
        restaurant_id= i) 
        review.append(review1)
        resto = restaurant[i]
        kastoma = customer[i]
        #resto.restaurants.append(kastoma)

    # review = [Review(
    #     star_rating = random.randint(1,6),
    #     comment = fake.sentence(),
    #     customer_id = i,
    #     restaurant_id= i        
    # ) for i in range(50)]
    # print("After")

    # for i in range(1, 50):
    #     resto = restaurant[i]
    #     kastoma = customer[i]
    #     resto.customers.append(kastoma)
        

    # session.query(review).delete() #clear table
    session.add_all(customer)
    session.commit()

    session.add_all(restaurant)
    session.commit()

    session.add_all(review)
    session.commit()

    print("start test")
    review1 = session.query(Review).get(1)
    print(review1)
    print("Done")

