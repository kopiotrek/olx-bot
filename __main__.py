from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException
from undetected_chromedriver import Chrome, ChromeOptions
import time
import os.path
import readchar
import xml.etree.ElementTree as ET
from xml.dom import minidom

# CONFIG HERE
# searching_url = "https://www.olx.pl/praca/dostawca-kurier-miejski/"
# searching_url = "https://www.olx.pl/praca/dostawca-kurier-miejski/?search%5Bfilter_enum_type%5D%5B0%5D=parttime&search%5Bfilter_enum_experience%5D%5B0%5D=exp_no&search%5Bfilter_enum_special_requirements%5D%5B0%5D=student_status&search%5Bfilter_enum_agreement%5D%5B0%5D=zlecenie"
searching_url = "https://www.olx.pl/praca/inne-oferty-pracy/"

mainBrowser = Chrome()

class OlxBot:
    def __init__(self):
        self.is_authenticated = False

    # def sendMessage(offer_url):
    #     print("Message is sending!")
    #     main_window = mainBrowser.current_window_handle
    #     mainBrowser.execute_script("window.open();")
    #     print("Window handles length:", len(mainBrowser.window_handles))
    #     mainBrowser.switch_to.window(mainBrowser.window_handles[0])
    #     mainBrowser.get(offer_url)
    #     message_url = mainBrowser.find_element(By.XPATH,"//*[@id=\"contact_methods\"]/li[1]/a").get_attribute('href')
    #     mainBrowser.get(message_url)
    #     message_text_area = mainBrowser.find_element(By.XPATH,"//*[@id=\"ask-text\"]")
    #     message_text_area.send_keys(messageString)
    #     print("Your action needed!")
    #     print("Please tell us if the captcha exists, Write yes or no and press enter")
    #     user_key_1 = readchar.readkey()
    #     if user_key_1 == 'y' or user_key_1 == 'Y':
    #         print("Please solve captcha and press enter!")
    #         input()
    #         submit_button = mainBrowser.find_element(By.XPATH,
    #             "//*[@id=\"contact-form\"]/fieldset/div[4]/div/span/input")
    #     elif user_key_1 == 'n' or user_key_1 == 'N':
    #         submit_button =  mainBrowser.find_element(By.XPATH,
    #             "//*[@id=\"contact-form\"]/fieldset/div[3]/div/span/input")
    #     submit_button.click()
    #     time.sleep(5)
    #     mainBrowser.close()
    #     mainBrowser.switch_to.window(main_window)


    def readJobApplicationData(self):
        try:
            tree = ET.parse('job_application_data.xml')
        except:
            print("ERROR: File 'job_application_data.xml' not found")
            return False
        root = tree.getroot()
        name = ""
        surname = ""
        phone = ""
        cv_file_path = ""
        message = ""
        for child in root:
            if child.tag == 'name':
                name = child.text
            elif child.tag == 'surname':
                surname = child.text
            elif child.tag == 'phone':
                phone = child.text
            elif child.tag == 'cv_file_path':
                cv_file_path = child.text
            elif child.tag == 'message':
                message = child.text
            elif child.tag == 'expected_salary':
                expected_salary = child.text
        print(f"Name: {name}")
        print(f"Surname: {surname}")
        print(f"Phone: {phone}")
        print(f"CV File Path: {cv_file_path}")
        print(f"Message: {message}")
        jobApplicationData = [name, surname, phone,
                              cv_file_path, message, expected_salary]

        return jobApplicationData


    def sendJobApplication(self,offer_url):
        jobApplicationData = self.readJobApplicationData()
        if jobApplicationData is False:
            return False
        mainBrowser.execute_script("window.open();")
        mainBrowser.switch_to.window(mainBrowser.window_handles[0])
        mainBrowser.get(offer_url)
        try:
            # Press "Aplikuj"
            mainBrowser.find_element(By.CLASS_NAME, "css-ezafkw").click()
            # mainBrowser.get(application_url)
            time.sleep(2)

            firstName_text_field = mainBrowser.find_element(By.NAME, "firstName")
            firstName_text_field.send_keys(jobApplicationData[0])
            lastName_text_field = mainBrowser.find_element(By.NAME, "lastName")
            lastName_text_field.send_keys(jobApplicationData[1])
            phoneNumber_text_field = mainBrowser.find_element(
                By.NAME, "phoneNumber")
            phoneNumber_text_field.send_keys(jobApplicationData[2])
            # try:
            #     mainBrowser.find_element(
            #         By.XPATH, "//*[@data-testid=\"attach-cv\"]").click()
            #     fileInput = mainBrowser.find_element(
            #         By.CSS_SELECTOR, "input[data-testid='applyform-cv-upload-input']")
            #     fileInput.send_keys(jobApplicationData[3])
            # except:
            #     print("ERROR: CV already submitted for this offer")
            #     return
            message_text_field = mainBrowser.find_element(By.NAME, "message")
            message_text_field.clear()
            message_text_field.send_keys(jobApplicationData[4])
            time.sleep(2)
            # Click "Aplikuj" second time
            mainBrowser.find_element(By.CLASS_NAME, "css-g8papo").click()
            time.sleep(4)
            job_start_time_radio_button = mainBrowser.find_element(
                By.XPATH, "//input[@type='radio' and @value='now']")
            job_start_time_radio_button.click()
            time.sleep(2)
            experience_radio_button = mainBrowser.find_element(
                By.XPATH, "//input[@type='radio' and @value='yes_over_year']")
            experience_radio_button.click()
            time.sleep(2)
            expected_salary_text_field = mainBrowser.find_element(
                By.NAME, "5b37098a-a46b-4893-a687-2ec7a31e27d3")
            expected_salary_text_field.send_keys(jobApplicationData[5])
            # Click "Wyślij odpowiedzi"
            time.sleep(2)
            mainBrowser.find_element(By.CLASS_NAME, "css-dekqtb").click()
            # Click "Kontynuuj wyszukiwanie"
            time.sleep(2)
            mainBrowser.find_element(By.CLASS_NAME, "css-17rpsjk").click()
            print("Application sent!")
            return True
        except:
            self.addToXML(offer_url, "failed_attempts.xml", "url")
            print("Application for a job failed, url saved in 'failed_attempts.xml' file")

        return False


    def addToXML(self,offer_url, file_name, class_name):
        if os.path.exists(file_name):
            tree = ET.parse(file_name)
            root = tree.getroot()
        else:
            root = ET.Element(file_name)
            tree = ET.ElementTree(root)
        url_element = ET.Element(class_name)
        url_element.text = offer_url
        root = tree.getroot()
        root.append(url_element)

        tree.write(file_name, encoding='utf-8', xml_declaration=True)

        # Pretty print the XML
        with open(file_name, "w", encoding='utf-8') as f:
            f.write(self.prettifyXML(root))


    def prettifyXML(elem):
        """Return a pretty-printed XML string for the Element."""
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


    def getNextPageUrl(self):
        print("Changing to next page")
        try:
            next_button_url = mainBrowser.find_element(
                By.XPATH, "//*[@data-testid='pagination-forward']").get_attribute('href')

            print(next_button_url)
            return next_button_url
        except NoSuchElementException as exception:
            print("Its last page!")
            self.mainTab()


    def additionalOfferInfo(offer_url):
        print("Printing description of a offer")
        print("------------------------------")
        additional_browser = Chrome()
        additional_browser.get(offer_url)
        offer_description = additional_browser.find_element(
            By.XPATH, "//*[@id=\"textContent\"]").text
        additional_browser.close()
        return offer_description


    def askUserDoesHeWant(self,offer_url):
        print("If you want it, press Y, else N. For offer description I. For link L. To open it in your browser press O")
        user_key = readchar.readkey()
        if user_key == "y" or user_key == 'Y':
            if self.is_authenticated == 'Not logged in':
                print("You cannot send messages when you aren't logged in")
                print("Press B to come back to main tab and log in")
                user_key = readchar.readkey()
                if user_key == "B" or "b":
                    self.mainTab()
                self.askUserDoesHeWant(offer_url, self.is_authenticated)
            else:
                print("Input: Yes")
                offer_database = open("offerDatabase.txt", "a")
                offer_database.write(offer_url)
                offer_database.close()
                self.sendJobApplication(offer_url)
        elif user_key == 'n' or user_key == 'N':
            print("Input: No")
            offer_database = open("offerDatabase.txt", "a")
            offer_database.write(offer_url)
            offer_database.close()
        elif user_key == 'i' or user_key == 'I':
            print("------------------------------")
            print(self.additionalOfferInfo(offer_url))
            self.askUserDoesHeWant(offer_url, self.is_authenticated)
        elif user_key == 'l' or user_key == 'L':
            print(offer_url)
            self.askUserDoesHeWant(offer_url, self.is_authenticated)
        elif user_key == "o" or user_key == "O":
            additional_browser = Chrome()
            additional_browser.get(offer_url)
            print("Press enter when you're done")
            input()
            additional_browser.close()
            self.askUserDoesHeWant(offer_url, self.is_authenticated)
        elif user_key == readchar.key.CTRL_C:
            print("Bye")
            mainBrowser.exit()
            exit()
        else:
            self.askUserDoesHeWant(offer_url, self.is_authenticated)


    def checkIfFileContainsString(string_to_search):
        offer_database = open("offerDatabase.txt", "r")
        for line in offer_database:
            if string_to_search in line:
                offer_database.close()
                return True


    def getListOffers(self, mode):
        if self.is_authenticated == 'Not logged in':
            print("NOT LOGGED IN, you can't send messages to sellers")
        print("Getting list of offers")
        array_offer_names = mainBrowser.find_elements(By.CLASS_NAME, "css-13gxtrp")

        for offerName in array_offer_names:
            print("------------------------------")
            # if checkIfFileContainsString(offerName.get_attribute('href')):
            #     print("One offer has been skipped!")
            # else:
            print(offerName.text)
            # print(offerPrice.text)
            if mode != "skipAsk":
                self.askUserDoesHeWant(offerName.get_attribute(
                    "href"), self.is_authenticated)
        mainBrowser.get(self.getNextPageUrl(self.is_authenticated))
        self.getListOffers(self.is_authenticated, mode)


    def readAccountData(self):
        try:
            tree = ET.parse('account_data.xml')
        except:
            print("ERROR: File 'account_data.xml' not found")
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
        time.sleep(3)
        mainBrowser.find_element(By.ID, "onetrust-accept-btn-handler").click()
        moj_olx_button_url = mainBrowser.find_element(
            By.XPATH, "//*[@data-cy='myolx-link']").get_attribute('href')
        print("Logging using predefined login and password")
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
                print("Logging in is taking so much time, please fix your password in config")
                exit()
        print("Logged in!")
        print("------------------------------")
        self.is_authenticated = True


    def settingsTab(self):
        print("Settings tab here")
        print("------------------------------")
        print("1. Add new messages")
        print("2. Change login")
        print("3. Edit saved offers")
        print("4. Come back to main tab")
        user_key = readchar.readkey()
        if user_key == '1':
            print("1")
        elif user_key == '2':
            print("2")
        elif user_key == '3':
            print("3")
        elif user_key == '4':
            self.mainTab()


    def mainTab(self):
        if os.path.isfile("offerDatabase.txt") == 0:
            print("offerDatabase.txt doesn't exist. Creating it")
            offer_database = open("offerDatabase.txt", "w")
            offer_database.close()
        if self.is_authenticated is False:
            print("------------------------------")
            print("Hello, program has been made by gbaranski")
            print("Its used to manage OLX.pl and make your life easier :)")
            print("------------------------------")
            print("What would you like to do today?")
        # print("1. Auth me on OLX. NEEDED TO SEND MESSAGES! Currently: " + self.is_authenticated)
        print("2. Search for new offers")
        print("3. Search for new offers - no user input")
        print("4. Settings")
        self.doAuth()
        user_key = readchar.readkey()
        if user_key == '1':
            # doAuth()
            print("Log in is automatic")
        elif user_key == '2':
            mainBrowser.get(searching_url)
            self.getListOffers(self.is_authenticated, 'nocriteria')
        elif user_key == '3':
            mainBrowser.get(searching_url)
            self.getListOffers(self.is_authenticated, 'skipAsk')
        elif user_key == '4':
            self.settingsTab(self.is_authenticated)
        elif user_key == readchar.key.CTRL_C:
            print("Bye")
            exit()
        else:
            print("Select proper key")
            self.mainTab()


bot = OlxBot()
bot.mainTab()
