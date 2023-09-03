from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))



username='hrvatar@outlook.com'
password='@sialkot1'

##############   LOGIN  ################################
driver.get("https://employers.indeed.com/")
# #driver.refresh()
usernameField = driver.find_element(By.XPATH,"//*[@id='ifl-InputFormField-3']")
usernameField.send_keys(username) #### YOUR LINKEDIN USERNAME 

# usernameField.send_keys(Keys.RETURN)
# passwordField = driver.find_element(By.ID,"session_password")
# passwordField.send_keys(password) #### YOUR LINKEDIN PASSWORD
# passwordField.send_keys(Keys.RETURN)



###################### JOB POST ###################################