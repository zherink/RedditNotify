from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import os
import smtplib, ssl
import time
import json

def look_for_new_post():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    driver.get('https://www.reddit.com/user/ashtonisVULCAN_IW/posts/')
    
    links = None
    i = 0
    while links == None:
        try:
            links = driver.find_elements_by_class_name('SQnoC3ObvgnGjWt90zD9Z')
        except:
            time.sleep(1)
            i = i + 1
            if i == 20:
                driver.quit()
                print('driver could not get links')
                exit()
    
    link = links[0].get_attribute('href')
    post = links[0].text
    driver.quit()
    with open('postid.json', 'r') as json_file:
        data = json.load(json_file)
        if data['postId'] != post:
            try:
                msg = '{} {}'.format(post, link)
                print(msg)
                send_message(msg)
            except:
                print('could not send message to Zach')

            with open('postid.json', 'w') as json_file:
                data = {'postId' : post}
                json.dump(data, json_file)


def send_message(msg):
    msg = msg.replace('https://', '')
    port = 465
    email_password = os.getenv('ETEXT_PASS')
    email_sender = os.getenv('ETEXT_EMAIL')
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', port, context=context)
    try:
        server.login(email_sender, email_password)
    except:
        print('could not sign in to email')
    server.sendmail(email_sender, os.getenv('ETEXT_ZACH'), msg)

if not os.path.isfile('postid.json'):
    f = open('postid.json', 'w')
    data = {'postId' : ''}
    json.dump(data,f)
    f.close()

look_for_new_post()
