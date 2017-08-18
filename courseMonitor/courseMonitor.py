import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import time


def get_open_seats(subject,course,section):
    URL = 'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept='+subject+'&course='+course+'&section='+section
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    courses = {}
    
    for row in soup.find_all('tr'):
        cols = [e.text for e in row.find_all('td')]
        if cols:
            if cols[0] == 'General Seats Remaining:':
                general = {'general':int(cols[1])}
                courses.update(general)

            if cols[0] == 'Restricted Seats Remaining*:':
                restricted = {'restricted':int(cols[1])}
                courses.update(restricted)
    return courses

account_sid = "AC1e8afac286908f2faf3163108dd90dc8"
auth_token = "9e58e584f3ede5b2313bdeb29469c53f"
phone_from = "+16047061473"
phone_to   = "+16043633930"
client = Client(account_sid, auth_token)

message_temp = "Great news, there is open seat in "

if __name__ == '__main__':
    subject = 'STAT'
    course  = '406'
    section = '101'
    course_str = subject + " " + course + " " + section
    while 1:
        courses = get_open_seats(subject,course,section)
        print("monitoring: " + course_str)
        if courses["restricted"] != 0 or courses["general"] != 0:
            message = message_temp+ course_str + " General: " + str(courses["general"]) + " Restricted: " + str(courses["restricted"])
            send = client.api.account.messages.create(to=phone_to,
                                                      from_=phone_from,
                                                      body=message)
            break
        time.sleep(60)
