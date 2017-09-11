import requests
from bs4 import BeautifulSoup
import time
import json
import copy
from resturant import resturant
import re

base_URL    = 'https://www.yelp.ca/'
start_point = 'search?cflt=restaurants&find_loc=Vancouver%2C+BC%2C+Canada'

def get_rest(number):
    re          = requests.get(base_URL+start_point)
    soup        = BeautifulSoup(re.text, 'html.parser')
    rest_list   = []
    
    while len(rest_list) < number:
        rest_list      += get_rest_at_current_page(soup)
        next_page_link =  get_next_page(soup)
        re             =  requests.get(base_URL+next_page_link)
        soup           =  BeautifulSoup(re.text, 'html.parser')
    
    return rest_list

def get_rest_at_current_page(soup):
    restList = []
    for entries in soup.find_all("li", { "class" : "regular-search-result" }):
        rest = get_rest_from_entry(entries)
        restList.append(rest)
    return restList

def get_rest_from_entry(entry):
    address          = entry.find("address").text.strip()
    name             = entry.find("span",{"class":"indexed-biz-name"}).find("span").text.strip()
    phone            = entry.find("span",{"class":"biz-phone"}).text.strip()
    price            = entry.find("span",{"class":"price-range"})

    if price:
        price = price.text
    else:
        prcie = "unknown"

    rating           = entry.find("div",{"class":"i-stars"})['title']
    review_count_str = entry.find("span",{"class":"review-count rating-qualifier"}).text.strip()
    review_count     = re.sub("[^0-9]", "", review_count_str)
    rest             = resturant(name,address,rating,review_count,price,phone)
    return rest

def get_next_page(soup):
    page_link = soup.find("a",{"class":"u-decoration-none next pagination-links_anchor"}).get('href')
    return page_link

if __name__ == '__main__':
    rl = get_rest(100)
    
    re_file = open("resturants.txt", "w")
    for r in rl:
        re_file.write(str(r))

    re_file.close()
