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

class Ticket:
    def __init__(self, webobject=None, email=None):

        self.webobject = webobject
        self.email = email if self.webobject == None else self.get_mail()

    def get_mail(self):
        '''Param web_object: An Identity validation ticket 
        .. Type web_object: Web Object
        .. Return: the mail that is contained into the name of the ticket
        .. rtype: String
        .. rtype: Boolean'''
        raw = str(self.webobject.text)
        mail = ''

        if "from " in raw:
            mail = raw.split("from ")[1]
        else:
            mail = raw.split("user ")[1]
        return mail

    def return_to_main(func):
        '''
        after closing a ticket, waits 1 second and return to principal window
        '''
        def wrapper(self):
            value = func(self)
            time.sleep(1)
            invgate.open_tkts()
            return value
        return wrapper

    @return_to_main
    def close_invgate(self):
        try:
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, self.email))).click()
            # WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_time'))).click()
            # WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID,'result_time'))).send_keys('5')
            # WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@title='Select a category']"))).click()
            # WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Work [Real Time]']"))).click()
            # WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'button-silver'))).click()
            # if check_exists(By.ID,'popup_option_yes'):
            #     DRIVER.find_element(By.ID, 'popup_option_yes').click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'request_toolbar_menu'))).click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Solve']"))).click()
            DRIVER.switch_to.frame(WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@title='Rich Text Editor, reply_textarea']"))))
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, '//body//p'))).send_keys('-')
            DRIVER.switch_to.default_content()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'submit_button'))).click()
            time.sleep(2)
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@title='Select an option']"))).click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Glober no respondió')]"))).click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'submit-button'))).click()

        except TimeoutException:
            print('No hay tickets para cerrar, continuaré con google admin')

    def close_admin(self):

        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).clear()
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(self.email)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']"))).send_keys(Keys.ENTER)
        try:
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Select all rows']"))).click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ow30']"))).click()
            time.sleep(1)
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete Devices')]"))).click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Delete')]"))).click()
        except:
            print(f'el mail {self.email} había sido eliminado anteriormente')

class Platform:
    '''Either Invgate or google admin '''

    def __init__(self, username, password, url):

        self.username = username
        self.password = password
        self.url = url
        
    def open(self):
        DRIVER.get(self.url)

    def switch(self):
        '''opens a new tab with the url of the platform'''

        DRIVER.execute_script("window.open('about:blank', 'secondtab');")
        DRIVER.switch_to.window("secondtab")
        self.open()

class Invgate(Platform):

    def login(self):

        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'login_username'))).send_keys(self.username)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'login_password'))).send_keys(self.password)
        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'button_login'))).click()
    
    def open_tkts(self):

        WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.ID, 'sidebar_requests'))).click()
        if check_exists(By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"):
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"))).click()
        else: 
            print("Todos los tickets de ID validation fueron cerrados")

class Admin(Platform):

    def login(self):

        WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='identifierId']"))).send_keys(self.username)
        WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.ID, 'identifierNext'))).click()
        WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(self.password)
        WebDriverWait(DRIVER, 10).until(EC.visibility_of_element_located((By.ID, 'passwordNext'))).click()
        time.sleep(8)

    def open_tkts(self):
        '''open google admin and then go to "devices" '''

        self.login()
        DRIVER.get("https://admin.google.com/ac/devices/list?status=6&category=all")

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

def scroll():

    HTML = DRIVER.find_element(By.TAG_NAME, 'html') #this variable is used to interact with the html
    HTML.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    HTML.send_keys(Keys.PAGE_UP)

#initializing variables
INVG_USER, INVG_PASS = config('INVG_USER'), config('INVG_PASS')
ADMIN_USER, ADMIN_PASS = config('ADMIN_USER'), config('ADMIN_PASS')
invgate = Invgate(INVG_USER, INVG_PASS, 'https://globant.cloud.invgate.net/')
admin = Admin(ADMIN_USER, ADMIN_PASS, 'https://admin.google.com/')
PATH = "C:\\Users\\Juan\\Desktop\\Proyectos\\Work_automation\\tickets_backup.txt"
DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tickets = []

if __name__ == "__main__":

    #Open invgate and get mails
    invgate.open()
    invgate.login()
    invgate.open_tkts()
    scroll()

    try:
        raw_tickets = WebDriverWait(DRIVER, 5).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT,'@globant.com')))
        for web_object in raw_tickets:
            tickets.append(Ticket(web_object))

    except TimeoutException:
        print('No hay tickets en la cola actualmente, revisando si existen tickets de procesos anteriores...')

    #checks if exists backup
    if(os.path.exists(PATH)): 
        with open('tickets_backup.txt', 'r') as tickets_backup:
            for line in tickets_backup:
                # Remove linebreak which is the last character of the string
                curr_place = line[:-1]
                tickets.append(Ticket(email = curr_place))
                
    #create file and fills it
    with open('tickets_backup.txt', 'w') as tickets_backup:
        for ticket in tickets:
            tickets_backup.write(f'{ticket.email}\n')

    #si no hay tickets en invgate/(o sea si no está el boton de id) esto se va a repetir la cantidad de veces segun tickets haya, una perdida de tiempo
    if check_exists(By.XPATH, "//span[normalize-space()='Globant - GIST Identity Validation']"):
        for ticket in tickets: ticket.close_invgate()
    
    admin.switch()
    admin.open_tkts()
    for ticket in tickets: ticket.close_admin()

    os.remove(PATH)#Deletes tickets_backup.txt