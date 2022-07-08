import google_auth_oauthlib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time, datetime, random,sys
from credentials import Email, User
import smtplib
from billiard.pool import Pool
from otpRetriever import *
import datetime
import pandas as pd
from amazon_biz import DebitCard

class AmazonID:
    def __init__(self, email, password, phoneNumber):
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber

def clickRep(browser, xpath):
    times = 1
    while times<30:
        try:
            browser.find_element_by_xpath(xpath).click()
            break
        except Exception as e:
            print(e)
            time.sleep(0.5)
            times += 1
    if times>=30:
        raise Exception("Sorry, no numbers below zero")

def typeRep(browser, xpath, typeValue):
    times = 1
    while times<30:
        try:
            browser.find_element_by_xpath(xpath).send_keys(typeValue)
            break
        except Exception as e:
            print(e)
            time.sleep(0.5)
            times += 1
    if times>=30:
        raise Exception("Sorry, no numbers below zero")

def getTextRep(browser, xpath):
    times = 1
    while times<30:
        try:
            return browser.find_element_by_xpath(xpath).text
        except Exception as e:
            print(e)
            time.sleep(0.5)
            times += 1
    if times>=30:
        raise Exception("Sorry, no numbers below zero")

def funcCall(amazonId):
    options = Options()
    options.set_headless(headless=False)
    b1 = webdriver.Firefox(firefox_options=options)
    b1.get("'https://www.amazon.in/ap/signin?openid.assoc_handle=inflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0'")

    while 1:
        try:
            b1.find_element_by_xpath('''//*[@id="ap_email"]''')
            break
        except:
            b1.refresh()
            time.sleep(5)

    b1.find_element_by_xpath('''//*[@id="ap_email"]''').send_keys(amazonId.email, Keys.RETURN)
    time.sleep(2)
    b1.find_element_by_xpath('''//*[@id="ap_password"]''').send_keys(amazonId.password, Keys.RETURN)
    time.sleep(2)

    clickRep(b1, '//*[@id="nav-link-yourAccount"]')
    clickRep(b1, '(//*[@class="b-card b-clickable b-block"])[1]')

    i = 1
    while 1:
        try:
            orderDate = getTextRep(b1, f'((//*[@class="a-box a-color-offset-background order-info"])[{i}]//span[@class="a-color-secondary value"])[1]')
            orderAmount = getTextRep(b1, f'(//*[@class="a-box a-color-offset-background order-info"])[{i}]//span[@class="currencyINRFallback"]')
            i += 1
        except:
            break

if __name__ == '__main__':
    """ This script is executed, when you run .py file. """

    #4718650900029049 Oswal@1234

    email_csv = pd.read_csv('./email_info.csv')

    email_list = []
    for ind,row in email_csv.iterrows():
        amazonId = AmazonID(row.email, row.password, row.phoneNumber)
        email_list.append(amazonId)

    account_entries = []
    pool = Pool(8)
    account_entries = account_entries.append(pool.map_async(funcCall, email_list))
    pool.close()
    pool.join()

    today_date = datetime.date.today()
    last_date = today_date - datetime.timedelta(days=7)
    start_date = last_date - datetime.timedelta(days=7)

    path_name = f'./accounts_from_{start_date.day}-{start_date.month}-{start_date.year}_to_{last_date.day}-{last_date.month}-{last_date.year}'
    account_entries.to_csv(path_name)
