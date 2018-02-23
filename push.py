import dotenv
from stravalib.client import Client
from datetime import datetime
from datetime import timedelta
import smtplib
from stravalib import unithelper
from email.mime.text import MIMEText
import calendar

def main():
    now = datetime.utcnow()
    start = get_range_start(now)
    end = datetime(now.year, now.month, 1, 0, 0, 1)
    
    dotenv.load()
    total_miles = get_total_miles(start, end, dotenv.get("STRAVA_TOKEN"))

    message = "Total Mileage for month of {0}: {1} miles".format(calendar.month_name[get_prev_month(now)], total_miles)

    send_email(message, dotenv.get("EMAIL_TO"), dotenv.get("EMAIL_FROM"), dotenv.get("EMAIL_PWD"))

def get_range_start(now):
    prev_month = get_prev_month(now)
    first_of_prev_month = now.replace(day=1).replace(month=prev_month)
    end = first_of_prev_month - timedelta(days=1)
    return datetime(end.year, end.month, end.day, 23, 59, 59)

def get_prev_month(now):
    return (now.replace(day=1) - timedelta(days=1)).month

def get_total_miles(start, end, token):
    dotenv.load()
    client = Client(dotenv.get("STRAVA_TOKEN"))

    total_miles = 0
    for activity in client.get_activities(after=start, before=end):
        total_miles += unithelper.miles(activity.distance).num
    
    return int(total_miles)

def send_email(msg, email_to, email_from, email_pwd):
    email = MIMEText(msg)
    email['Subject'] = "Monthly Mileage"
    email['From'] = email_from
    email['To'] = email_to

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_from, email_pwd)

    server.sendmail(email_from, email_to, email.as_string())
    server.quit()

main()


