import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time
import json
import copy

account_sid = "ACccaaa3e15321dc811ac50aeef6de8bb4"
auth_token = "72b347d88956ec7b733a9e562c146d15"
phone_from = "+16047061261"
client = Client(account_sid, auth_token)
message_temp = "Great news, there is open seat in "

def get_open_seats(subject,course,section):
    URL = 'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept='+subject+'&course='+course+'&section='+section
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    courses = {}
    
    for row in soup.find_all('tr'):
        cols = [e.text for e in row.find_all('td')]
        if cols:
            if cols[0] == 'Total Seats Remaining:':
                seat_num = {'seat':int(cols[1])}
                courses.update(seat_num)

    return courses

def update():
    with open("subscribeList.json", "r") as slr:
        sub_list = json.load(slr)
    
    subcribe_list = copy.deepcopy(sub_list)
    course_list   = subcribe_list.keys()

    print(course_list)
    
    for course in course_list:
        element = course.split(",")
        seat    = get_open_seats(element[0],element[1],element[2])
        if seat["seat"] != 0:
            for phone_to in subcribe_list.get(course):
                message = message_temp+ course + " available seat: " + str(seat["seat"])
                send    = client.api.account.messages.create(to=phone_to,
                                                          from_=phone_from,
                                                          body=message)
            del sub_list[course]

    with open("subscribeList.json", "w") as slw:
        json.dump(sub_list, slw)
    return

if __name__ == '__main__':
    while 1:
        update()
        time.sleep(60)
