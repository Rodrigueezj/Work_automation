import pytest
from Invgate import Ticket, backup
class TestClass:
    webobject = <selenium.webdriver.remote.webelement.WebElement (session="c7641a59111a026fbfa8d13f93b34364", element="c349027a-a894-4de1-8d9b-60f2829ef09d")
    ticket = Ticket()
    tickets = []
    def get_mail_test(self):
        mail = self.ticket.get_mail()
        assert mail == 'suraj.varade@globant.com'

    def backup_test(self):
        pass

    get_mail_test()