import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 1.3521 # SG's latitude, float
MY_LONG = 103.8198 # SG's longitude, float

#TODO =========== ISS Overhead ============
def overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    print(data)

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    PARAMS = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=PARAMS)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    now = datetime.now().hour
    # Before splitting --> 2023-01-13T11:15:49+00:00
    # sunset = (d["results"]["sunset"]).split("T") --> prints as ['2023-01-13', '11:15:49+00:00']
    if now >= sunset or now <= sunrise:
        return True

#TODO ============= EMAIL SETUP ==============
gmail = "dummy@gmail.com"
gmail_pw = "dummypw"

while True:
    time.sleep(20)
    if overhead() and is_night():
        with smtplib.SMTP(host = "smtp.gmail.com", port = 587) as connection: #this statement automatically closes off the connection once the email has been sent
            connection.starttls()  # makes connection secure
            connection.login(user = gmail, password = gmail_pw)
            connection.sendmail(
                from_addr = gmail,
                to_addrs = "dummy@gmail.com",
                msg = f"Subject: Look up!\n\nIt's a bird, it's a plane, it's the ISS!"
                )
        print("Ding dong, the email has been sent")



