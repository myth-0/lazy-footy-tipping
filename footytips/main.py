import argparse
import requests
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import sys
from pathlib import Path


def sendTipsviaEmail(tips, config):
    sender_email = f"{config['smtp_email']}"
    password = f"{config['smtp_app_password']}"

    receiver_email = sender_email

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Footy Tips for round {tips['round']}"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html_content = f"Footy Tips for round {tips['round']}"
    del tips["round"]
    html_content += "<table>"
    for key, value in tips.items():
        html_content += f"<tr><td><strong>"
        html_content += f"{key}</strong></td><td>{value}</td></tr>"
    html_content += "</table>"

    msg.attach(MIMEText(html_content, "html"))
    # Attach parts into message container.

    # Server configuration
    smtp_server = f"{config['smtp_server']}"
    smtp_server_port = int(f"{config['smtp_server_port']}")
    # Send the message via iCloud SMTP server.
    try:
        server = smtplib.SMTP(smtp_server, smtp_server_port)
        server.ehlo()  # Identify the client to the server
        server.starttls()  # Upgrade the connection to SSL/TLS
        server.ehlo()  # Re-identify the client over the secure connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def validateResponse(resp):
    if resp.status_code == 200:
        return True
    else:
        return resp.status_code


def main(args, config, noEmail):
    # Use command-line arguments in your program
    year = args.year
    # API endpoint URL
    if noEmail:
        config["UserAgent_AppName"] = input(
            "Enter User Agent App Name (Shared with Squiggle): "
        )
        config["UserAgent_ContactEmail"] = input(
            "Enter User agent Contact Email (Shared with Squiggle): "
        )
    headers = {
        "User-Agent": f"{config['UserAgent_AppName']} ({config['UserAgent_ContactEmail']})"
    }

    getround = f"https://api.squiggle.com.au/?q=games;complete=0;year={year}"

    response = requests.get(getround, headers=headers)
    round: str = ""

    if validateResponse(response):
        data = response.json()
        round = data["games"][0]["round"]

    tipsurl = f"https://api.squiggle.com.au/?q=tips&year=2024&round={round}&source=8"
    print(f"Round is {round}")
    # Check if the request was successful
    response = requests.get(tipsurl, headers=headers)
    if validateResponse(response):
        data = response.json()
        tipsdict = {}
        data["tips"] = sorted(data["tips"], key=lambda tip: tip["date"])
        for tip in data["tips"]:
            print(f"Tip: {tip['tip']}")
            tipsdict[f"{tip['hteam']} vs. {tip['ateam']}"] = tip["tip"]

        tipsdict["round"] = f"{round}"
        if not noEmail:
            sendTipsviaEmail(tipsdict, config)
        else:
            print("Thank you! Bye")


def configExists(configPath):
    return Path(configPath).exists()


def createConfig(configPath):
    # Prompt the user for each field
    smtp_server = input("Enter SMTP Server Address: ")
    smtp_server_port = input("Enter SMTP Server Port: ")
    smtp_email = input("Enter SMTP email: ")
    smtp_app_password = input("Enter SMTP app-specific password: ")
    receiver_email = input("Enter receiver email: ")
    UserAgent_AppName = input("Enter User Agent App Name: ")
    UserAgent_ContactEmail = input("Enter User Agent Contact Email: ")

    # Create a dictionary with the input values
    data = {
        "smtp_server": smtp_server,
        "smtp_server_port": smtp_server_port,
        "smtp_email": smtp_email,
        "receiver_email": receiver_email,
        "smtp_app_password": smtp_app_password,
        "UserAgent_AppName": UserAgent_AppName,
        "UserAgent_ContactEmail": UserAgent_ContactEmail,
    }

    # Write the data to a JSON file
    with open(configPath, "w") as f:
        json.dump(data, f, indent=4)
        return


if __name__ == "__main__":
    thisYear = str(datetime.date.today().year)
    parser = argparse.ArgumentParser(description="Do some footy tipping")
    parser.add_argument("--year", type=str, default=thisYear, help="")
    parser.add_argument("--no-email", action="store_true")

    configData = {}
    args = parser.parse_args()
    if not args.no_email:
        configPath = f"{sys.path[0]}/../config.json"

        if not configExists(configPath):
            createConfig(configPath)

        with open(configPath, "r") as file:
            configData = json.load(file)

    main(args, configData, args.no_email)
