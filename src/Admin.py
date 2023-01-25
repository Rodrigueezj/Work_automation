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
    def __init__(self, email=None):
        self.email = email

    def close_admin(self):
        search = WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Search by keyword or serial number']")))
        search.clear()
        search.send_keys(self.email)
        search.send_keys(Keys.ENTER)

        try:
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Select all rows']"))).click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ow30']"))).click()
            time.sleep(1)
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Delete Devices')]"))).click()
            WebDriverWait(DRIVER, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Delete')]"))).click()
        except:
            print(f'el usuario {self.email} había sido eliminado anteriormente')

class Admin:
    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

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

def backup(path, tickets):  
        #checks if exists backup
        if(os.path.exists(path)): 
            with open('tickets_backup.txt', 'r') as tickets_backup:
                for line in tickets_backup:
                    # Remove linebreak which is the last character of the string
                    curr_place = line[:-1]
                    tickets.append(Ticket(email = curr_place))

#initializing variables
ADMIN_USER, ADMIN_PASS = config('ADMIN_USER'), config('ADMIN_PASS')
admin = Admin(ADMIN_USER, ADMIN_PASS, 'https://admin.google.com/')
PATH = "C:\\Users\\Juan\\Desktop\\Proyectos\\Work_automation\\tickets_backup.txt"
DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
tickets = []

if __name__ == "__main__":
    backup(PATH, tickets) #Checks mails
    DRIVER.get(admin.url)
    admin.open_tkts()
    for ticket in tickets: ticket.close_admin()
    os.remove(PATH)#Deletes tickets_backup.txt