import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from decouple import config

def check_exists(option , id):
    '''Param option: The kind of locator that identifies the web object 
    .. Type option: By.locator
    .. Param id: Name of the web object locator 
    .. Type id: String
    .. Return: Wether the web object exists or not
    .. Rtype: Boolean'''

    try:
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located(((option, id))))
    except TimeoutException:
        return False
    return True

def login(username, password):

    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'login_username'))).send_keys(username)
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'login_password'))).send_keys(password)
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'button_login'))).click()

def login_admin(username, password):

    WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='identifierId']"))).send_keys(username)
    WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.ID, 'identifierNext'))).click()
    WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password)
    WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.ID, 'passwordNext'))).click()
    time.sleep(8)

def get_mail(web_object):
    '''Param web_object: An Identity validation ticket 
    .. Type web_object: Web Object
    .. Return: the mail that is contained into the name of the ticket
    .. rtype: String
    .. rtype: Boolean'''

    raw = str(web_object.text)
    mail = ''

    if "from " in raw:
        mail = raw.split("from ")[1]
    else:
        mail = raw.split("user ")[1]
    return mail

def open_id_tickets():

    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'sidebar_requests'))).click()
    if check_exists(By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"):
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"))).click()
    else: 
        print("Todos los tickets de ID validation fueron cerrados")

def return_to_main(func):
    def wrapper(*args):
        value = func(args)
        time.sleep(1)
        open_id_tickets()
        return value
    return wrapper

@return_to_main            
def charge_and_close(mail):
    '''Param mail: Mail of the user whose ticket will be closed 
    .. Type mail: Parameter and its variable type
    .. Return: None'''
    
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, mail))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_time'))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID,'result_time'))).send_keys('5')
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@title='Select a category']"))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Work [Real Time]']"))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'button-silver'))).click()
    if check_exists(By.ID,'popup_option_yes'):
        DRIVER.find_element(By.ID, 'popup_option_yes').click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_menu'))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='dropDownWindow']//a[@id='time_solve_action']"))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'popup_option_no'))).click()
    DRIVER.switch_to.frame(WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='Rich Text Editor, reply_textarea']"))))
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, '//body//p'))).send_keys('-')
    DRIVER.switch_to.default_content()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'submit_button'))).click()
    time.sleep(2)
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Select an option']"))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Glober no respondió')]"))).click()
    WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'submit-button'))).click()

def close_admin(mails):

    for mail in mails:
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).clear()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(mail)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(Keys.ENTER)
        try:
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Select all rows']"))).click()
        except:
            continue
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ow30']"))).click()
        time.sleep(1)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete Devices')]"))).click()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Delete')]"))).click()

#initializing variables
INVG_USER, INVG_PASS = config('INVG_USER'), config('INVG_PASS')
ADMIN_USER, ADMIN_PASS = config('ADMIN_USER'), config('ADMIN_PASS')
PATH = "C:\\Users\\Juan\\Desktop\\Work_automation\\src\\mails_backup.txt"
DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
mails = []

if __name__ == "__main__":
    #Open invgate and get mails 
    DRIVER.get("https://globant.cloud.invgate.net/")
    login(INVG_USER, INVG_PASS)
    open_id_tickets()
    HTML = DRIVER.find_element(By.TAG_NAME, 'html') #this variable is used to interact with the html to scroll up and down the page
    HTML.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    HTML.send_keys(Keys.PAGE_UP)

    try:
        raw_tickets = WebDriverWait(DRIVER, 5).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,'@globant.com')))
        for mail in raw_tickets:
            mails.append(get_mail(mail))
    except TimeoutException:
        raw_tickets = []

    #checks if exists backup
    if(os.path.exists(PATH)): 
        with open('mails_backup.txt', 'r') as mails_backup:
            for line in mails_backup:
                # Remove linebreak which is the last character of the string
                curr_place = line[:-1]
                # Add item to the list
                mails.append(curr_place)

    #create file and fills it
    with open('mails_backup.txt', 'w') as mails_backup:
        for mail in mails:
            mails_backup.write(f'{mail}\n')

    print(mails)
    for mail in mails:
        charge_and_close(mail)
        
    DRIVER.execute_script("window.open('about:blank', 'secondtab');")
    DRIVER.switch_to.window("secondtab")
    DRIVER.get('https://admin.google.com/')
    login_admin(ADMIN_USER, ADMIN_PASS)
    DRIVER.get("https://admin.google.com/ac/devices/list?status=6&category=all")
    close_admin(mails)
    os.remove(PATH)