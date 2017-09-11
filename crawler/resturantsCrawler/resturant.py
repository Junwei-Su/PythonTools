import requests
from bs4 import BeautifulSoup
import time
import json
import copy

class resturant:
    
    def __init__(self, name, address, rating, reviews_count, price, phone):
        self.name           = name
        self.rating         = rating
        self.address        = address
        self.reviews_count  = reviews_count
        self.price          = price
        self.phone          = phone

    def __str__(self):
        return str(self.name) + "," + str(self.rating) + "," + str(self.address) + "," + str(self.reviews_count) + "," + str(self.price) + "," + str(self.phone) + "\n"
