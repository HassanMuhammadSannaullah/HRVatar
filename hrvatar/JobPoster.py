from exchangelib import Credentials, DELEGATE, Account
import re
from html import unescape


import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def PostJob(title, skills, Description, Country, State=None):
    username = "hrvatar@outlook.com"
    # Initialize the WebDriver with WebDriverManager
    driver = webdriver.Chrome(
        service=Service(executable_path=ChromeDriverManager().install())
    )

    wait = WebDriverWait(driver, 10)

    driver.get("https://www.jobisite.com/postFreeJob.htm")

    # Title
    title_element = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="title"]'))
    )
    title_element.send_keys(title)

    # Skills
    skills_element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/div/div[2]/form/div/div[3]/div/div[2]/input')
        )
    )
    skills_element.send_keys(skills)

    # Description
    description_element = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="discription"]'))
    )
    description_element.send_keys(Description)

    viewport_height = driver.execute_script("return window.innerHeight")

    # Scroll down by half the viewport height
    driver.execute_script(f"window.scrollBy(0, {viewport_height / 2});")

    # Country
    country_element = wait.until(
        EC.presence_of_element_located((By.XPATH, f'//option[@value="{Country}"]'))
    )
    country_element.click()

    # State
    if State:
        state_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f'//*[@id="state"]/option[@value="{State}"]')
            )
        )
        state_element.click()

    # Email
    email_element = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email1"]'))
    )
    email_element.send_keys(username)

    # Calculate the halfway point of the page's vertical scroll height
    scroll_height = driver.execute_script(
        "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
    )
    halfway = scroll_height / 2

    # Scroll to the halfway point
    driver.execute_script(f"window.scrollTo(0, {halfway});")

    # # Post on Other Boards option
    # post_on_other_boards_element = wait.until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, '//*[@id="content"]/div/div[2]/form/div/div[8]/div/div[2]/input')
    #     )
    # )
    # post_on_other_boards_element.click()

    # Captcha
    captcha = driver.find_element(By.XPATH, '//*[@id="txtCaptchaDiv"]').text
    driver.find_element(By.XPATH, '//*[@id="txtInput"]').send_keys(captcha)

    time.sleep(5)
    # Submit Button
    driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div[2]/form/div/div[11]/div/div[2]/a'
    ).click()

    # time.sleep(10)
    # # Outlook credentials
    # outlook_email = "hrvatar@outlook.com"
    # outlook_password = "@hassansana1"

    # # Set up Exchange credentials
    # credentials = Credentials(username=outlook_email, password=outlook_password)

    # # Connect to the Outlook account
    # account = Account(
    #     primary_smtp_address=outlook_email,
    #     credentials=credentials,
    #     autodiscover=True,
    #     access_type=DELEGATE,
    # )

    # # Access the inbox
    # inbox = account.inbox

    # # Get the latest email
    # latest_email = inbox.filter().order_by("-datetime_received")[0]

    # # Print the email subject and body
    # email_subject = latest_email.subject
    # email_body = latest_email.text_body

    # # Define a regular expression pattern to match URLs containing "serviceFreeJobActivate"
    # url_pattern = r'https?://[^\s<>"]*serviceFreeJobActivate[^\s<>"]*'

    # # Use re.findall to extract all matching URLs from the email body
    # verification_links = re.findall(url_pattern, unescape(email_body))

    # # Print the verification links
    # for link in verification_links:
    #     print(link)

    return "done"
