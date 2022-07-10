""" Libraies need to run script."""
from this import d
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

now = datetime.datetime.now()

class DebitCard:
    def __init__(self, cardName, cardNumber, expMonth, expYear, cvv, staticPass):
        self.cardName = cardName
        self.cardNumber = cardNumber
        self.expMonth = expMonth
        self.expYear = expYear
        self.cvv = cvv
        self.staticPass = staticPass

class AmazonID:
    def __init__(self, email, password, phoneNumber):
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber

class OrderEntry:
    def __init__(self, link, AmazonID, DebitCard, poNumber):
        self.link = link
        self.AmazonID = AmazonID
        self.DebitCard = DebitCard
        self.poNumber = poNumber

class Product:
    """ Product class with helper functions. """
    
    def __init__(self,**kwargs):
        """ Constructor function of Product class. 
        Delay is set to random to avoid detection by amazon which
        could result in temporarily block. """
        tempUser = User()
        tempUser.UNAME = kwargs['amazon_id'].email
        tempUser.PASSWD = kwargs['amazon_id'].password
        self.amazon_credential = tempUser
        # self.email_credential = Email()
        self.product = kwargs['p_url']
        self.debitCard = kwargs['debit_card']
        self.amazonId = kwargs['amazon_id']
        self.poNumber = kwargs['po_number']
    
    def print(self, x):
        print(f"{now.time()} ----- {self.amazon_credential.UNAME} ------ {x}")

    def clickRep(self, xpath):
        times = 1
        while times<30:
            try:
                self.browser_emulator.find_element_by_xpath(xpath).click()
                break
            except Exception as e:
                if times==29:
                    print(e)
                time.sleep(0.5)
                times += 1
        if times>=30:
            raise Exception("Sorry, no numbers below zero")

    def typeRep(self, xpath, typeValue):
        times = 1
        while times<30:
            try:
                self.browser_emulator.find_element_by_xpath(xpath).send_keys(typeValue)
                break
            except Exception as e:
                if times==29:
                    print(e)
                time.sleep(0.5)
                times += 1
        if times>=30:
            raise Exception("Sorry, no numbers below zero")


    def buyUsingCreditCard(self):
        #SelectableAddCreditCard
        #time.sleep(2)
        #self.browser_emulator.find_element_by_xpath('//*[@value="SelectableAddCreditCard"]').click()
        self.clickRep('//*[@value="SelectableAddCreditCard"]')
        self.print("Next Continue done.")

        # #pp-uIL6vG-89
        #time.sleep(2)
        #self.browser_emulator.find_element_by_xpath('//*[@name="ppw-accountHolderName"]').send_keys(self.debitCard.cardName)
        self.typeRep('//*[@name="ppw-accountHolderName"]', self.debitCard.cardName)
        self.print("name")
        #self.browser_emulator.find_element_by_xpath('//*[@name="ppw-expirationDate_month"]/..').click()
        #self.browser_emulator.find_element_by_xpath(f'(//*[@data-value="{self.debitCard.expMonth}"])').click()
        self.clickRep('//*[@name="ppw-expirationDate_month"]/..')
        self.clickRep(f'(//*[@data-value="{self.debitCard.expMonth}"])')
        self.print("month")
        #self.browser_emulator.find_element_by_xpath('//*[@name="ppw-expirationDate_year"]/..').click()
        #self.browser_emulator.find_element_by_xpath(f'(//*[@data-value="{self.debitCard.expYear}"])').click()
        self.clickRep('//*[@name="ppw-expirationDate_year"]/..')
        self.clickRep(f'(//*[@data-value="{self.debitCard.expYear}"])')
        self.print("year")
        #self.browser_emulator.find_element_by_xpath('//*[@name="addCreditCardNumber"]').send_keys(self.debitCard.cardNumber)
        self.typeRep('//*[@name="addCreditCardNumber"]', self.debitCard.cardNumber)
        self.print("number")
        #(//*[@name="ppw-widgetEvent:AddCreditCardEvent"])
        #self.browser_emulator.find_element_by_xpath('(//*[@name="ppw-widgetEvent:AddCreditCardEvent"])').click()
        self.clickRep('(//*[@name="ppw-widgetEvent:AddCreditCardEvent"])')
        self.print("Card found and Added")

        time.sleep(10)

        i = 0
        while i<50:
            self.print(i)
            try:
                self.browser_emulator.find_element_by_xpath("//*[@name=\"addCreditCardVerificationNumber" + str(i) + "\"]").send_keys(self.debitCard.cvv)
                self.browser_emulator.find_element_by_xpath("(//input[@type=\"checkbox\"])[" + str(i+1) + "]").click()
                break
            except:
                i += 1
                continue
        self.print("CVV Done & box cheked!")

    def buyUsingEMI(self):
        self.clickRep('//*[@value="instrumentId=EMI&isExpired=false&paymentMethod=CC&tfxEligible=false"]')
        self.clickRep('(//*[@class="a-button-text a-declarative"])//*[text()="Select EMI options"]')
        self.clickRep('//*[@data-value="EMI-SelectableAddCreditCard"]')
        self.typeRep('//*[@name="ppw-accountHolderName_EMI"]', self.debitCard.cardName)

        self.clickRep('(//*[@class="a-dropdown-prompt"])[last()-1]/../..')
        self.clickRep(f'//*[@id="2_dropdown_combobox"]/li//*[@data-value="{self.debitCard.expMonth}"]')

        self.clickRep('(//*[@class="a-dropdown-prompt"])[last()]/../..')
        time.sleep(1)
        self.clickRep(f'//*[@id="3_dropdown_combobox"]/li//*[@data-value="{self.debitCard.expYear}"]')

        self.typeRep('//*[@name="addCreditCardNumber_VCC"]', self.debitCard.cardNumber)
        
        self.clickRep('//*[@name="ppw-widgetEvent:AddEmiCreditCardEvent"]')

        time.sleep(10)

        i = 0
        while i<50:
            self.print(i)
            try:
                self.browser_emulator.find_element_by_xpath("//*[@name=\"addCreditCardVerificationNumber" + str(i) + "\"]").send_keys(self.debitCard.cvv)
                break
            except:
                i += 1
                continue
        self.print("CVV Done & box cheked!")

        time.sleep(6)

        i=1
        while 1:
            self.print(i)
            if i==50:
                break
            try:
                self.browser_emulator.find_element_by_xpath("(//span[contains(.,\"Select EMI Tenure\")])[" + str(i) + "]").click()
                #self.browser_emulator.find_element_by_xpath('(//*[@class="a-fixed-left-grid a-spacing-mini"])[last()]/../div[3]/span').click()
                #self.browser_emulator.find_element_by_xpath("(//*[text()=\"Select EMI Tenure\"])[" + str(i) + "]").click()
                print()
                break
            except Exception as e:
                print(e)
                i += 1
                continue
        
        time.sleep(2)
        self.clickRep('((//*[@class="a-popover a-popover-modal"])//*[text()="No Cost"])[last()]')
        time.sleep(2)

        i=1
        while 1:
            self.print(i)
            if i==1000:
                break
            try:
                self.browser_emulator.find_element_by_xpath("((//*[@class=\"a-popover a-popover-modal\"])//span[contains(.,\"Choose EMI Plan\")])[" + str(i) + "]").click()
                break
            except Exception as e:
                print(e)
                i += 1
                continue
        time.sleep(2)
        

    def launch_bot(self):
        """ Initializes bot and emulates selenium browser. 
        It goes to login page first. """

        try:
            options = Options()
            options.set_headless(headless=False)
            self.browser_emulator = webdriver.Firefox(firefox_options=options, executable_path="/usr/local/bin/geckodriver")
        except Exception as e:
            print(e)
        
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        
        # self.browser_emulator = webdriver.Chrome(chrome_options=chrome_options)




        self.browser_emulator.get\
        ('''https://www.amazon.in/ap/signin?openid.assoc_handle=inflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0''')
        
    def user_login_session(self):
        """ Enter user credentials and goto product page. """

        while 1:
            try:
                self.browser_emulator.find_element_by_xpath('''//*[@id="ap_email"]''')
                break
            except:
                self.browser_emulator.refresh()
                time.sleep(5)


        self.browser_emulator.find_element_by_xpath\
        ('''//*[@id="ap_email"]''').send_keys(self.amazon_credential.UNAME,Keys.RETURN)
        time.sleep(2)
        self.browser_emulator.find_element_by_xpath\
        ('''//*[@id="ap_password"]''').send_keys(self.amazon_credential.PASSWD,Keys.RETURN)
        time.sleep(2)
        
        """ Change this URL to add another product to cart. """
        self.browser_emulator.get(self.product)
        #self.browser_emulator.get\('''https://www.amazon.in/OnePlus-Bullets-Wireless-Earphones-Black/dp/B07D3FN6QM/''')
        
    def check_availability(self):
        """ This function checks product availability
        and adds it to cart when possible. """
        
        try:
        	self.browser_emulator.find_element_by_xpath\
            ('''//*[@id="add-to-cart-button"]''')
        
        except:
            try:
            	self.browser_emulator.find_element_by_xpath\
                ('''//*[@id="priceblock_dealprice"]''')
            except:
                try:
                    self.browser_emulator.find_element_by_xpath\
                    ('''//*[@id="priceblock_saleprice"]''')
                except:
                    pass
                else:
                    self.add_to_cart()
            else:
                self.add_to_cart()

        else:
            self.add_to_cart()
            
        finally:
            #self.browser_emulator.refresh()
            #time.sleep(10)
            self.print('It is not is Stock yet.')
            self.browser_emulator.quit()

    def add_to_cart(self):
        """ Helper function to add product to cart."""
        self.print("Buy button reached!")

        try:
            self.browser_emulator.find_element_by_xpath('//*[@class="a-checkbox a-checkbox-fancy aok-inline-block checkBoxCSS"]/label/i').click()
            self.print("Coupon Selected!")
        except:
            self.print("No Coupon!")

        
        #self.browser_emulator.find_element_by_xpath('//*[@id="add-to-cart-button"]').click()
        #self.email_notification()
        self.clickRep('//*[@id="add-to-cart-button"]')
        self.print("Added to cart by buy button!!")

        #attach-close_sideSheet-link
        time.sleep(3)
        try:
            self.browser_emulator.find_element_by_xpath('//*[@id="attach-close_sideSheet-link"]').click()
            self.print("Went to Cart!")
        except:
            self.print("no acc pop ups")

        #time.sleep(2)
        #self.browser_emulator.find_element_by_xpath('//*[@id="nav-cart"]').click()
        self.clickRep('//*[@id="nav-cart"]')
        self.print("Went to Cart!")

        #proceedToRetailCheckout
        #time.sleep(2)
        #self.browser_emulator.find_element_by_xpath('//*[@name="proceedToRetailCheckout"]').click()
        self.clickRep('//*[@name="proceedToRetailCheckout"]')
        self.print("Checkout page....")

        self.typeRep('//*[@id="cof-text-input-value-0"]', self.poNumber)

        #a-autoid-0-announce
        #time.sleep(5)
        #self.browser_emulator.find_element_by_xpath('//*[@id="a-autoid-0"]').click()
        self.clickRep('//*[@id="a-autoid-0"]')
        self.print("Continue button!")

        #address-book-entry-0
        #time.sleep(2)
        #self.browser_emulator.find_element_by_xpath('(//div[@id="address-book-entry-0"]/div[2]/span)[1]').click()
        self.clickRep('(//div[@id="address-book-entry-0"]/div[2]/span)[1]')
        self.print("Address Selected....")

        #//input[@type="checkbox"]
        time.sleep(1)

        try: 
            self.browser_emulator.find_element_by_xpath('//input[@type="checkbox"]').click()
            print("service checkbox unselected")
        except:
            print("no service button")
            pass

        #sosp-continue-button a-button a-button-primary a-button-span12 a-padding-none  continue-button 
        #time.sleep(2)
        #self.browser_emulator.find_element_by_xpath('(//input[@value="Continue"])[1]').click()
        self.clickRep('(//input[@value="Continue"])[1]')
        self.print("Next Continue done.")

        try:
            self.buyUsingEMI()
        except:
            self.buyUsingCreditCard()
        

        #######
        #(//*[text()="No Cost"])
        #((//*[@class="a-popover a-popover-modal"])[last()]//*[text()="No Cost"])[last()]
        ########

        

        #ppw-widgetEvent:SetPaymentPlanSelectContinueEvent
        #self.browser_emulator.find_element_by_xpath('//*[@name="ppw-widgetEvent:SetPaymentPlanSelectContinueEvent"]').click()
        self.clickRep('//*[@name="ppw-widgetEvent:SetPaymentPlanSelectContinueEvent"]')
        self.print("Continued...")

        # prime-interstitial-nothanks-button
        try:
            time.sleep(2)
            self.browser_emulator.find_element_by_xpath('//*[@id="prime-interstitial-nothanks-button"]').click()
        except Exception as e:
            self.print(e)
            self.print("No prime")
            pass

        # placeYourOrder1
        time.sleep(15)

        try:
            #self.browser_emulator.find_element_by_xpath('//*[@id="placeYourOrder"]')
            #.click()
            self.clickRep('//*[@id="placeYourOrder"]')
            self.print("Order Placed!! HahaHa!")
        except:
            self.print("Failwa!")

        time.sleep(5)

        try: 
            self.browser_emulator.find_element_by_xpath('(//input[@value="Continue"])[1]').click()
            print("continue")
        except:
            print("No page after place order....")
            pass

        time.sleep(5)

        try: 
            self.browser_emulator.find_element_by_xpath('(//div[@id="address-book-entry-0"]/div[2]/span)[1]').click()
            print("address")
        except:
            print("No address page after place order....")
            pass

        time.sleep(5)

        try: 
            self.browser_emulator.find_element_by_xpath('//*[@id="placeYourOrder"]').click()
            print("place order")
        except:
            print("No place order page after place order....")
            pass

        # staticAuthOpen
        time.sleep(5)
        self.browser_emulator.find_element_by_xpath('//*[@id="staticAuthOpen"]').click()
        self.print("Static Auth....")
        #txtPassword
        self.browser_emulator.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(self.debitCard.staticPass)
        self.print("Entered static Pass!")
        # self.browser_emulator.find_element_by_xpath('//*[@id="cmdSubmitStatic"]').click()
        # self.print("Payment Done!!")

        # time.sleep(30)

        self.browser_emulator.quit()

def multiCall(orderEntry):

    linkTo = orderEntry.link
    amazonId = orderEntry.AmazonID
    debitCard = orderEntry.DebitCard
    poNumber = orderEntry.poNumber

    print(f"Call id : {linkTo} ----- {amazonId.email}")
    product = linkTo
    bot = Product(p_url=product, amazon_id = amazonId, debit_card = debitCard, po_number = poNumber)
    bot.launch_bot()
    bot.user_login_session()
    bot.check_availability()

if __name__ == '__main__':
    """ This script is executed, when you run .py file. """

    print(f"Start Time : {now.time()}")

    csv_file = pd.read_csv('./data.csv')

    # debitCards = [DebitCard('oswal trading', '4042760719465628', '9', '2022', '915', 'Oswal@1234')]
    # ids = [
    #           AmazonID('oswaltrading901@gmail.com', 'oswal@1234', '0'),
    #         AmazonID('oswaltrading903@gmail.com', 'oswal@1234', '0'),
    #         AmazonID('oswaltrading902@gmail.com', 'oswal@1234', '0'),
    #         AmazonID('oswaltrading904@gmail.com', 'oswal@1234', '0'),
    #         #AmazonID('oswaltrading905@gmail.com', 'oswal@1234', '0'),
    #         # AmazonID('oswaltrading906@gmail.com', 'oswal@1234', '0'),
    #         # AmazonID('oswaltrading907@gmail.com', 'oswal@1234', '0'),
    #         # AmazonID('oswaltrading908@gmail.com', 'oswal@1234', '0')
    #         ]

    csv_file = csv_file.iloc[:,:11].dropna()
    argsTuple = []
    for ind,row in csv_file.iterrows():
        #print(row.staticPass)
        debitCard = DebitCard(row.cardName, row.cardNumber, row.expMonth, row.expYear, row.cvv, row.staticPass)
        amazonId = AmazonID(row.email, row.password, row.phoneNumber)
        orderEntry  = OrderEntry(row.link, amazonId, debitCard, row.poNumber)
        argsTuple.append(orderEntry)

    #argsTuple = [OrderEntry("https://www.amazon.in/Apple-iPhone-13-128GB-Midnight/dp/B09G9HD6PD/ref=sr_1_1?crid=36PE1RR5TWQ8N&keywords=iphone13&qid=1656267544&sprefix=iphone13%2Caps%2C225&sr=8-1", i, debitCards[0]) for i in ids]
    pool = Pool(1)
    pool.map_async(multiCall, argsTuple)


    pool.close()
    pool.join()

    # product = sys.argv[1]
    # bot = Product(p_url=product)
    # bot.launch_bot()
    # bot.user_login_session()
    # while 1:
    #     bot.check_availability()

        

        