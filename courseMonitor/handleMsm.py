from flask import Flask, request
import redis
from twilio.twiml.messaging_response import MessagingResponse
import json


twilio_account_sid = 'AC*****'
my_number = '+****'

app = Flask(__name__)

def respond(user, body):
    response = MessagingResponse()
    response.message(body=body)
    return str(response)

@app.route('/sms', methods=['POST'])
def handle_sms():
    user        = request.form['From']
    course      = request.form['Body'].strip().upper()
    new_entry   = {str(course):str(user)}
    with open("subscribeList.json", "r") as slr:
        sub_list = json.load(slr)

    user_list = sub_list.get(course)
    if user_list:
        entry.append(user)
        sub_list.update({course:user_list})
    else:
        sub_list.update({course:[user]})

    with open("subscribeList.json", "w") as slw:
        json.dump(sub_list, slw)
    
    return respond(user, body="Sweet action. We are now monitoring "+course+" for you and will let you know when there are seats available")

if __name__ == '__main__':
    app.run(debug=True)
