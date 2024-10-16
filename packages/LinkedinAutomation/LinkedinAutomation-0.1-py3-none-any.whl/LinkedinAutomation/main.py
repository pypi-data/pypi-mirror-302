import io
import os
import time
import socket
import pickle
import polars as pl
import pandas as pd
from github import Github
from dotenv import load_dotenv
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

load_dotenv()

def help():
    print(f"""Hello {os.getlogin().title()}!\U0001F60A,

Thank you for choosing the LinkedinAutomation package. We sincerely appreciate your support.

Should you require any assistance or have any questions, please do not hesitate to reach out to Ranjeet Aloriya at +91 940.660.6239 or ranjeet.aloriya@gmail.com. We are here to help!

Cheers!
Ranjeet Aloriya""")
    
    
def removeconnection(u_name, pswd, start_from, checked, removed, chrome_driver):
    print(f"""Hello {os.getlogin().title()}!\U0001F60A,

Thank you for your support of my Python module! I appreciate your enthusiasm and feedback.

I want to inform you that I am currently working on a new version to address some issues with the current release. I apologize for any inconvenience this may cause and appreciate your understanding during this process.

Should you require any assistance or have any questions, please do not hesitate to reach out to Ranjeet Aloriya at +91 940.660.6239 or ranjeet.aloriya@gmail.com. We are here to help!

Cheers!
Ranjeet Aloriya""")