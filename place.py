import csv
from functions import procces, write_to_csv


class Place:
    places = []

    def __init__(self, name, website, address, phone_no, categories, ratings, services_offered, search_query):
        self.name = name
        self.website = website
        self.address = address
        self.phone_no = phone_no
        self.categories = categories
        self.ratings = ratings
        self.services_offered = services_offered
        self.search_query = search_query
        Place.places.append(self)

    def save_data(self, file):
        procces(f'writing data of {self.name}')
        write_to_csv(file, [self.name, self.website, self.address, self.phone_no, self.categories, self.ratings,
                            self.services_offered, self.search_query])
