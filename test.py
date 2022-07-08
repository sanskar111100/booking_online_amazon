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

def clickRep(browser, xpath):
        times = 1
        while times<30:
            try:
                browser.find_element_by_xpath(xpath).click()
                break
            except:
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
        except:
            time.sleep(0.5)
            times += 1
    if times>=30:
        raise Exception("Sorry, no numbers below zero")

if __name__ == '__main__':
    """ This script is executed, when you run .py file. """

    options = Options()
    options.set_headless(headless=False)
    browser_emulator = webdriver.Firefox(firefox_options=options)
    b2 = webdriver.Firefox(firefox_options=options)

    browser_emulator.get("https://netsafe.hdfcbank.com/ACSWeb/enrolljsp/HDFCValidate.jsp")


    ##########################################################################################################
   

    ##########################################################################################################

    #browser_emulator.execute_script("window.open('');")
    #browser_emulator.switch_to.window(browser_emulator.window_handles[1])
    b2.get('https://messages.google.com/web/authentication')
    # time.sleep(5)
    # browser_emulator.switch_to.window(browser_emulator.window_handles[0])
    # time.sleep(5)
    # browser_emulator.switch_to.window(browser_emulator.window_handles[1])
    # time.sleep(5)