from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, Column, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

BASE = declarative_base()

engine = create_engine("sqlite:///db/restaurant.db")
Session = sessionmaker(bind=engine)
session = Session()

restaurant_customer = Table(
    "restaurant_customers",
    BASE.metadata,
    Column('restaurant_id', ForeignKey("restaurants.id"), primary_key=True ),
    Column("customer_id", ForeignKey("customers.id"), primary_key=True),
    extend_existing=True
)


class Restaurant(BASE):
    __tablename__ = "restaurants"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    # print("xxxxxxxxxxxx")
    #one to many relationship: This is the parent
    reviews = relationship("Review", backref="restaurant", cascade=("all, delete"))
    # print("yyyyyyyyyy")
    customers = relationship("Customer", secondary=restaurant_customer, back_populates="restaurants")

    def all_reviews(self):
        restaurant_reviews = self.reviews
        review_list = []
        for rev in restaurant_reviews:
            xx = f"Review for {rev.restaurant.name} by {rev.customer.full_name()}: {rev.star_rating} stars."
            review_list.append(xx)
        return review_list
    
    #returns a list of all the reviews for the Restaurant
    def reviews(self):
        return self.reviews
    #returns a list of all the customers who reviewed the Restaurant
    #Lets first have all the reviews in our Restaurant
    #Out of those all those revies, lets search for customers who reviews the restaurant.
    def customers(self):
        all_customers = []
        restaurant_reviews = self.reviews
        for rest in restaurant_reviews:
            if rest not in all_customers:
                all_customers.append(rest.customer)
        return all_customers

    #returns one restaurant instance for the restaurant that has the highest price
    @classmethod
    def fanciest(cls):
        fanciest_resto = session.query(cls).order_by(cls.price[-1]).first()
        return fanciest_resto


class Customer(BASE):
    __tablename__ = "customers"

    id = Column(Integer(), primary_key=True)
    first_name =Column(String())
    last_name = Column(String())

    #One-many relationship: parent to child accessed parent.children
    #children will take foreignkey
    reviews = relationship("Review", backref="customer", cascade=("all, delete"))
    restaurants = relationship("Restaurant", secondary= restaurant_customer, back_populates="customers")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def favorite_restaurant(self):
        my_reviews = self.reviews
        my_list = sorted(my_reviews, key=lambda review: review.star_rating)     
        print(my_list[-1])  
        return my_list[-1]
    
    def add_review(self, restaurant, rating):
        # print(self.first_name)
        customer = session.query(Customer).filter_by(first_name = self.first_name).first()
        restaurant_inst = session.query(Restaurant).filter_by(name = restaurant.name).first()
        # print(customer_id)

        my_review = Review(comment="", star_rating=rating, customer_id= customer.id, restaurant_id = restaurant_inst.id)
        customer.restaurants.append(restaurant_inst)
        session.add(my_review)
        session.add(customer)
        session.commit()

    #return a list of all the reviews that the Customer has left
    def reviews(self):
        return self.reviews
    
    #return a list of all the restaurants that the Customer has reviewed
    def restaurants(self):
        all_restaurants = []
        all_reviews = self.reviews

        for rest in all_reviews:
            all_restaurants.append(rest.restaurant)
        return all_restaurants

    #removes all their reviews for this restaurant
    #delete rows from the reviews table
    def delete_reviews(self, restaurant):
        access_unique_key = [review.id for review in restaurant.reviews]
        if access_unique_key:
            item_deleted = delete(Review).where(Review.id.in_(access_unique_key))
            session.execute(item_deleted)
            session.commit()




class Review(BASE):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    comment = Column(String())
    star_rating = Column(Integer())

    #foreignKey assignment
    customer_id = Column(Integer(), ForeignKey("customers.id"))
    restaurant_id = Column(Integer(), ForeignKey("restaurants.id"))
    #inverse relationship
    # customer = relationship("Customer", backref="review", cascade=("all, delete"))
    #foreignKey assignment
    # restaurant_id = Column(Integer(), ForeignKey("customers.id"))
    #inverse relationship
    # restaurant = relationship("Restaurant", backref="review", cascade=("all, delete"))

    #return the Customer instance for this review
    #We have the virtual customer created from Customer class which is virtually in Review
    def customer(self):
        return self.customer


    #should return the Restaurant instance for this review
    #Restaurant has the virtual restaurant which is in Review.
    def restaurant(self):
        return self.restaurant

    #return a string formatted as follows
    def full_review(self):
        #Review for {insert restaurant name} by {insert customer's full name}: {insert review star_rating} stars.
        restaurant_name = self.restaurant.name
        customer_full_name =f"{self.first_name} {self.last_name}"
        rating = self.star_rating
        return f"Review for {restaurant_name} by {customer_full_name}: {rating} stars."





















