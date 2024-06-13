from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome
from termcolor import colored
import time
import os.path
import xml.etree.ElementTree as ET

mainBrowser = Chrome()


class OlxBot:
    def __init__(self):
        self.is_authenticated = False
        self.wait = WebDriverWait(mainBrowser, 20)  # Wait up to 20 seconds

    def readJobApplicationData(self):
        try:
            tree = ET.parse('job_application_data.xml')
        except:
            print(colored("ERROR: File 'job_application_data.xml' not found", 'red'))
            return False
        root = tree.getroot()
        name = ""
        surname = ""
        phone = ""
        cv_file_path = ""
        message = ""
        for child in root:
            if child.tag == 'search_url':
                search_url = child.text
            elif child.tag == 'name':
                name = child.text
            elif child.tag == 'surname':
                surname = child.text
            elif child.tag == 'phone':
                phone = child.text
            elif child.tag == 'email':
                email = child.text
            elif child.tag == 'cv_file_path':
                cv_file_path = child.text
            elif child.tag == 'message':
                message = child.text
            elif child.tag == 'expected_salary':
                expected_salary = child.text
        print(f"Search_url: {search_url}")
        print(f"Name: {name}")
        print(f"Surname: {surname}")
        print(f"Phone: {phone}")
        print(f"Email: {email}")
        print(f"CV File Path: {cv_file_path}")
        print(f"Message: {message}")
        self.jobApplicationData = [search_url, name, surname, phone, email,
                                   cv_file_path, message, expected_salary]

    def sendJobApplication(self, offer_url):

        mainBrowser.get(offer_url)
        try:
            # Press "Aplikuj"
            application_url = mainBrowser.find_element(
                By.CLASS_NAME, "css-ezafkw").get_attribute('href')

            olx_application_url = "/oferta/praca/aplikuj/"

            if olx_application_url.lower() in application_url.lower():
                mainBrowser.find_element(By.CLASS_NAME, "css-ezafkw").click()
            else:
                print(colored(
                    "ERROR: Application conducted via external website, url saved in 'failed_attempts.xml' file", 'red'))
                self.addToXML(offer_url,
                              "failed_attempts.xml", "ext_application"),
                return False

            # time.sleep(2)
            # Wait until the element is visible
            ok_button = self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "css-tory2h")))

            if ok_button.is_displayed():
                print(colored("------------------------------", 'red'))
                print(colored("Application limit reached.", 'red'))
                print(colored("------------------------------", 'red'))
                return "SHUTDOWN"

            message_text_field = mainBrowser.find_element(By.NAME, "message")
            message_text_field.clear()
            message_text_field.send_keys(self.jobApplicationData[6])
            # time.sleep(2)
            # Click "Aplikuj" second time
            apply_button = self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "css-g8papo")))
            apply_button.click()
            # mainBrowser.find_element(By.CLASS_NAME, "css-g8papo").click()
            # time.sleep(4)
            job_start_time_radio_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@type='radio' and @value='within_month']")))
            job_start_time_radio_button.click()
            # job_start_time_radio_button = mainBrowser.find_element(
            #     By.XPATH, "//input[@type='radio' and @value='within_month']")
            # job_start_time_radio_button.click()
            experience_radio_button = mainBrowser.find_element(
                By.XPATH, "//input[@type='radio' and @value='yes_over_year']")
            experience_radio_button.click()
            expected_salary_text_field = mainBrowser.find_element(
                By.NAME, "5b37098a-a46b-4893-a687-2ec7a31e27d3")
            expected_salary_text_field.send_keys(self.jobApplicationData[7])
            # Click "Wyślij odpowiedzi"
            mainBrowser.find_element(By.CLASS_NAME, "css-dekqtb").click()
            self.addToXML(offer_url, "sent_applications.xml", "url")
            print(colored("Application sent!", 'green'))

            return True
        except:
            self.addToXML(offer_url, "failed_attempts.xml", "error_url")
            print(colored(
                "ERROR: Application for a job failed, url saved in 'failed_attempts.xml' file", 'red'))

            return False

    def addToXML(self, offer_url, file_name, class_name):
        if os.path.exists(file_name):
            tree = ET.parse(file_name)
            root = tree.getroot()
        else:
            root = ET.Element('root')
            tree = ET.ElementTree(root)

        # Create a new element with the given class name and set its text to the offer URL
        url_element = ET.Element(class_name)
        url_element.text = offer_url

        # Append the new element to the root element
        root.append(url_element)

        # Write the tree back to the file with UTF-8 encoding and XML declaration
        tree.write(file_name, encoding='utf-8', xml_declaration=True)

    def isInXML(self, offer_url, file_name, class_name):
        if not os.path.exists(file_name):
            return False
        tree = ET.parse(file_name)
        root = tree.getroot()
        for elem in root.findall(class_name):
            if elem.text == offer_url:
                return True

        return False

    # def isInXML(offer_url, file_name, class_name):
    #     if not os.path.exists(file_name):
    #         return False
        
    #     tree = ET.parse(file_name)
    #     root = tree.getroot()
        
    #     def search_element(element):
    #         # Check if the current element matches the class name and contains the offer URL
    #         if element.tag == class_name and element.text == offer_url:
    #             return True
    #         # Recursively search within all child elements
    #         for child in element:
    #             if search_element(child):
    #                 return True
    #         return False
        
    #     return search_element(root)

    def getNextPageURL(self):
        try:
            next_button_url = mainBrowser.find_element(
                By.XPATH, "//*[@data-testid='pagination-forward']").get_attribute('href')
            return next_button_url
        except NoSuchElementException as exception:
            print(colored("Its last page!", 'yellow'))
            self.mainTab()

    def getListOffers(self, mode):
        if self.is_authenticated is False:
            print(colored("ERROR: You're not logged in", 'red'))
            return False
        print("------------------------------")
        print("Getting list of offers")
        print("------------------------------")

        array_offer_names = self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "css-13gxtrp")))
        array_offer_urls = []
        nextPageURL = self.getNextPageURL()
        for offerName in array_offer_names:
            newOfferURL = offerName.get_attribute('href')
            if self.isInXML(newOfferURL, "sent_applications.xml", "url"):
                print(
                    colored(f"{offerName.text} - skipped, already applied!", 'yellow'))
            elif self.isInXML(newOfferURL, "failed_attempts.xml", "ext_application"):
                print(
                    colored(f"{offerName.text} - skipped, known as exterior application website", 'yellow'))
            else:
                print(offerName.text)
                array_offer_urls.append(newOfferURL)
        try:
            for offerURL in array_offer_urls:
                if (self.sendJobApplication(offerURL) == "SHUTDOWN"):
                    return False
        except:
            print(
                colored("ERROR: Offers list has changed while applying for another.", 'red'))
        mainBrowser.get(nextPageURL)
        self.getListOffers(mode)

    def readAccountData(self):
        try:
            tree = ET.parse('account_data.xml')
        except:
            print(colored("ERROR: File 'account_data.xml' not found", 'red'))
            return False
        root = tree.getroot()
        login = ""
        password = ""
        for child in root:
            if child.tag == 'login':
                login = child.text
            elif child.tag == 'password':
                password = child.text
        print(f"Login: {login}")
        print(f"Password: {password}")
        accountData = [login, password]

        return accountData

    def doAuth(self):
        print("Attempting to log in")
        accountData = self.readAccountData()
        if accountData is False:
            return
        mainBrowser.get("https://www.olx.pl/")
        accept_button = self.wait.until(EC.presence_of_element_located(
            (By.ID, "onetrust-accept-btn-handler")))
        accept_button.click()
        moj_olx_button_url = mainBrowser.find_element(
            By.XPATH, "//*[@data-cy='myolx-link']").get_attribute('href')
        mainBrowser.get(moj_olx_button_url)
        mainBrowser.find_element(By.NAME, "username").send_keys(accountData[0])
        mainBrowser.find_element(By.NAME, "password").send_keys(accountData[1])
        mainBrowser.find_element(
            By.XPATH, "//*[@data-testid='login-submit-button']").click()

        i = 0
        while mainBrowser.current_url != "https://www.olx.pl/":
            i = i + 1
            time.sleep(1)
            print(".")
            if i > 15:
                print(
                    "Logging in is taking so much time, please fix your password in config")
                exit()
        print(colored("Logged in!", 'green'))
        print("------------------------------")
        self.is_authenticated = True

    def mainTab(self):
        print(colored("------------------------------", 'green'))
        print(colored("Starting OLX-BOT", 'green'))
        print(colored("------------------------------", 'green'))
        self.doAuth()
        self.readJobApplicationData()
        if self.jobApplicationData is False:
            print(
                colored("ERROR: Failed to read data from job_application_data.xml file", 'red'))
            return False
        if self.is_authenticated is True:
            mainBrowser.get(self.jobApplicationData[0])
            if (self.getListOffers('nocriteria') is False):
                print("Shutdown")


bot = OlxBot()
bot.mainTab()
