import dotenv
from stravalib.client import Client
from datetime import datetime
from datetime import timedelta
import smtplib
from stravalib import unithelper

def main():
    now = datetime.utcnow()
    start = end_of_month(now)
    end = datetime(now.year, now.month, 1, 0, 0, 1)
    
    dotenv.load()
    total_miles = get_total_miles(start, end, dotenv.get("STRAVA_TOKEN"))

    send_email(total_miles, dotenv.get("EMAIL_TO"), dotenv.get("EMAIL_FROM"), dotenv.get("EMAIL_PWD"))

def end_of_month(now):
    prev_month = (now.replace(day=1) - timedelta(days=1)).month
    first_of_prev_month = now.replace(day=1).replace(month=prev_month)
    end = first_of_prev_month - timedelta(days=1)
    return datetime(end.year, end.month, end.day, 23, 59, 59)

def get_total_miles(start, end, token):
    dotenv.load()
    client = Client(dotenv.get("STRAVA_TOKEN"))

    total_miles = 0
    for activity in client.get_activities(after=start, before=end):
        total_miles += unithelper.miles(activity.distance).num
    
    return int(total_miles)

def send_email(total_miles, email_to, email_from, email_pwd):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, email_pwd)

    msg = "Monthly Mileage: " + str(total_miles)
    server.sendmail(email_from, email_to, msg)
    server.quit()

main()


