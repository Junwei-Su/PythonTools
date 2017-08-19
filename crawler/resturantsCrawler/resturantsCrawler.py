import requests
from bs4 import BeautifulSoup
import time
import json
import copy

base_URL    = 'https://www.yelp.ca/'
start_point = 'search?cflt=restaurants&find_loc=Vancouver%2C+BC%2C+Canada'


def get_rest(number):
    re       = requests.get(base_URL+start_point)
    soup        = BeautifulSoup(re.text, 'html.parser')
    rest_list   = []
    
    while len(rest_list) < number:
        rest_list      += get_rest_at_current_page(soup)
        next_page_link =  get_next_page(soup)
        re             =  requests.get(base_URL+next_page_link)
        soup           =  BeautifulSoup(re.text, 'html.parser')
    
    return rest_list

def get_rest_at_current_page(soup):
    rest_name = []
    for entries in soup.find_all    ("li", { "class" : "regular-search-result" }):
        for ele in entries.find_all ("span",{"class":"indexed-biz-name"}):
            for name in ele.find    ("span"):
                rest_name.append(name)
    return rest_name

def get_next_page(soup):
    page_link = soup.find("a",{"class":"u-decoration-none next pagination-links_anchor"}).get('href')
    return page_link

if __name__ == '__main__':
    rl = get_rest(100)
    print(rl)
