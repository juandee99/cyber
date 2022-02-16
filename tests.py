from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from django.core.exceptions import ObjectDoesNotExist
import time
from selenium.common.exceptions import NoSuchElementException

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # així és com ho diu a la doc de Django
        # però necessitem una altra configuració pel mode headless
        #cls.selenium = WebDriver()
        #cls.selenium.implicitly_wait(5)
        opts = Options()
        opts.headless = False
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin123')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        # Aquesta localització de l'element ens serveix també a mode de ASSERT
        # Si no localitza l'element, ens donarà un NoSuchElementException
        self.selenium.find_element_by_xpath("//a[text()='Django administration']")
        time.sleep(3)
        self.selenium.find_element_by_xpath('//tr[@class="model-user"]//td//a[@class="addlink"][contains(text(),"Add")]').click()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('juande')
        password_input = self.selenium.find_element_by_name("password1")
        password_input.send_keys('Oscar.12')
        password_input = self.selenium.find_element_by_name("password2")
        password_input.send_keys('Oscar.12')
        time.sleep(3)
        self.selenium.find_element_by_name("_continue").click()
        self.selenium.find_element_by_name("is_staff").click()
        time.sleep(3)
        self.selenium.find_element_by_xpath('//option[@value="4"]').click()
        self.selenium.find_element_by_xpath('//a[@id="id_user_permissions_add_link"]').click()
        self.selenium.find_element_by_name("_save").click()
        time.sleep(3)
        self.selenium.find_element_by_xpath('//a[contains(text(),"Log out")]').click()
        time.sleep(3)
        self.selenium.find_element_by_xpath('//a[contains(text(),"Log in again")]').click()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('juande')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('Oscar.12')
        time.sleep(3)
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
#       self.selenium.find_element_by_xpath('//input[@value="Questions"]').click()
        self.selenium.find_element_by_xpath('//a[contains(text(),"Questions")]').click()
        time.sleep(2)
        self.selenium.find_element_by_xpath('//h1[contains(text(),"Select question to view")]')
        time.sleep(2)
#        self.selenium.find_element_by_xpath('//a[@class="addlink"]')

        try:
            self.selenium.find_element_by_xpath('//a[@class="addlink"]').click()
            raise Exception ("Menu add Question no encontroado")
        except NoSuchElementException:
            pass
#//a[contains(text(),'Add question')]
#//h1[contains(text(),'Select question to change')]
#//option[@value='4']
#//a[@id='id_user_permissions_add_link']
