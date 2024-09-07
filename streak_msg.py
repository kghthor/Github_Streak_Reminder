import os
import requests
from datetime import datetime
from twilio.rest import Client
 
# Twilio credentials
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_PHONE_NUMBER = ''
TO_PHONE_NUMBER = ''

# GitHub credentials
GITHUB_USERNAME = ''
GITHUB_TOKEN = ''  # If needed for authentication

# Reminder messages
REMINDER_MESSAGE = "Reminder: You haven't made any contributions to GitHub today. Don't break your streak!"
CONGRATULATIONS_MESSAGE = "Congratulations! You've made contributions to GitHub today. Keep up the good work! Consistency is the key."

# Setup Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to send SMS
def send_sms(message):
    message = twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print(f"SMS sent: {message.sid}")

# Function to check GitHub contributions
def has_contributed_today(username, token):
    today = datetime.now().date()
    url = f"https://api.github.com/users/{username}/events"
    headers = {'Authorization': f'token {token}'} if token else {}

    response = requests.get(url, headers=headers)
    events = response.json()

    for event in events:
        event_date = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ").date()
        if event_date == today:
            return True
    return False

# Main function
def main():
    # Check if there was a contribution today
    if has_contributed_today(GITHUB_USERNAME, GITHUB_TOKEN):
        send_sms(CONGRATULATIONS_MESSAGE)
    else:
        send_sms(REMINDER_MESSAGE)

if __name__ == '__main__':
    main()
