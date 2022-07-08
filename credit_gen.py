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

if __name__ == '__main__':
    """ This script is executed, when you run .py file. """

    options = Options()
    options.set_headless(headless=False)
    b1 = webdriver.Firefox(firefox_options=options)
    b2 = webdriver.Firefox(firefox_options=options)

    #4718650900029049 Oswal@1234

    b1.get("https://netsafe.hdfcbank.com/ACSWeb/enrolljsp/HDFCValidate.jsp")
    xcount = 0
    while 1:
        try:
            print("Trying to find.....", xcount)
            xcount += 1
            b1.find_element_by_xpath('(//*[@title="Generate NetSafe cards"])')
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    print("Looged in HDFC!")

    ##########################################################################################################

    b2.get("https://messages.google.com/web/authentication")
    clickRep(b2, '//*[@class="mdc-switch__handle"]')
    # time.sleep(20)
    # b2.refresh()
    while 1:
        try:
            b2.find_element_by_xpath('//*[@class="new-chat-header ng-star-inserted"]')
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    print("Logged in google messages!")

    ##########################################################################################################


    creditCardCsv = pd.DataFrame(columns = ['cardName', 'cardNumber', 'expMonth', 'expYear', 'cvv', 'staticPass'])

    cardAmount = 11240 #limit of each card
    staticPass = "Oswal@1234" #static pass word
    noOfCards = 5 #no of cards

    count = 0
    while count<noOfCards:
        #request time
        curTime = datetime.datetime.now()


        #request for a new card
        #/html/body/form/div/div[2]/div[3]/div/input
        #//*[@name="total"]
        b1.switch_to.frame(0)
        typeRep(b1, '//*[@name="total"]', cardAmount)
        clickRep(b1, '//*[@name="Go"]')
        print("New Card!")
        b1.switch_to.default_content()

        
        finalOtp = 0
        while 1:
            try: 
                #fetch OTP
                b2.refresh()
                #(//*[@class="name ng-star-inserted"])[1]
                #(//*[@class="ng-star-inserted"])[1]
                clickRep(b2, '(//*[@class="name ng-star-inserted"])[1]')
                otpMsg = getTextRep(b2, '(//*[@class="text-msg ng-star-inserted"])[last()]')
                print(f"Complete message - {otpMsg}")

                #parse OTP
                otp = otpMsg[21:27]
                print(f"OTP - {otp}")
                curDate = datetime.date.today()
                complete = f"{str(curDate.day)}/{str(curDate.month)}/{str(curDate.year)} " + otpMsg[83:91]
                print(f"Parsed date - {complete}")
                msgTime = datetime.datetime.strptime(complete, '%d/%m/%Y %H:%M:%S') - datetime.timedelta(seconds=589)
                print(curTime, msgTime)

                if curTime<msgTime:
                    finalOtp = otp
                    break
            except:
                continue

        #enter in hdfc textbox
        #exampleInputName2 id
        print(f"Final OTP - {finalOtp}")
        typeRep(b1, '//*[@id="exampleInputName2"]', finalOtp)
        #cmdSubmit id
        clickRep(b1, '//*[@id="cmdSubmit"]')

        #card details
        #(//*[@class="cardDesc"])/h5 card name
        cardName = getTextRep(b1, '(//*[@class="cardDesc"])/h5')
        #(//*[@class="cardDesc"])/label card no.
        cardNumber = getTextRep(b1, '(//*[@class="cardDesc"])/label')
        #(//*[@class="cvvDetails"])[2]/ul/li[1]/span cvv
        cardCvv = getTextRep(b1, '(//*[@class="cvvDetails"])[2]/ul/li[1]/span')
        #(//*[@class="cvvDetails"])[2]/ul/li[2]/span expiry date
        cardExpiry = getTextRep(b1, '(//*[@class="cvvDetails"])[2]/ul/li[2]/span')

        print(cardName, cardNumber, cardCvv, cardExpiry)

        #new Card
        #(//*[@title="Generate NetSafe cards"]) new card button
        clickRep(b1, '(//*[@title="Generate NetSafe cards"])')

        print("Card Generated haha!")

        expMonth = cardExpiry[0:2]
        if expMonth[0]=='0':
            expMonth = expMonth[1]
        expYear = "20" + cardExpiry[3:5]

        creditCardCsv.loc[len(creditCardCsv.index)] = [cardName, cardNumber, expMonth, expYear, cardCvv, staticPass] 
        count += 1
        time.sleep(30)

    creditCardCsv.to_csv('creditCards.csv')





