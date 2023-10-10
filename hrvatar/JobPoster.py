import time
import imaplib
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def PostJob(title, skills, Description, Country, State=None):
    # Initialize the WebDriver with WebDriverManager
    driver = webdriver.Chrome(
        service=Service(executable_path=ChromeDriverManager().install())
    )

    email = "hrvatar@outlook.com"
    password = "@hassansana1"
    joblink = ""

    driver.get("https://www.jobisite.com/postFreeJob.htm")
    # title
    driver.find_element(By.XPATH, '//*[@id="title"]').send_keys(title)

    # skills
    driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div[2]/form/div/div[3]/div/div[2]/input'
    ).send_keys(skills)

    # description
    driver.find_element(By.XPATH, '//*[@id="discription"]').send_keys(Description)

    # Country
    driver.find_element(By.XPATH, f'//option[@value="{Country}"]').click()

    # State
    if State:
        driver.find_element(
            By.XPATH, f'//*[@id="state"]/option[@value="{State}"]'
        ).click()

    # Email
    driver.find_element(By.XPATH, '//*[@id="email1"]').send_keys(email)

    # Post on Other Boards option
    driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div[2]/form/div/div[8]/div/div[2]/input'
    ).click()

    # Captcha
    captcha = driver.find_element(By.XPATH, '//*[@id="txtCaptchaDiv"]').text
    driver.find_element(By.XPATH, '//*[@id="txtInput"]').send_keys(captcha)

    time.sleep(2)
    # Submit Button
    driver.find_element(
        By.XPATH, '//*[@id="content"]/div/div[2]/form/div/div[11]/div/div[2]/a'
    ).click()

    time.sleep(10)

    mail = imaplib.IMAP4_SSL("outlook.office365.com")
    mail.login(email, password)
    mail.select("INBOX")

    # Search for the latest unread email
    typ, msg_ids = mail.search(None, "UNSEEN")
    msg_ids = msg_ids[0].decode().split()

    if msg_ids:
        # Mark the previous unread emails as seen
        for msg_id in msg_ids[:-1]:
            mail.store(msg_id, "+FLAGS", "\\Seen")

        msg_id = msg_ids[-1]  # Assuming the last email is the verification email

        # Fetch the email data
        typ, message_data = mail.fetch(msg_id, "(RFC822)")
        message_body = message_data[0][1]

        # Close the server connection
        mail.close()
        mail.logout()

        # Extract the verification code from the email body
        html_content = message_body.decode("utf-8")
        soup = BeautifulSoup(html_content, "html.parser")

        # Define a regular expression pattern to find URLs
        url_pattern = re.compile(r"https?://[^\s]+")

        # Find all URLs in the email body
        urls = url_pattern.findall(soup.get_text())

        # Filter the URLs to find the one that matches your expected format
        expected_url_pattern = re.compile(r"https://www\.jobisite\.com/sj/id/\d+-\w+")
        for url in urls:
            print(url)
            if expected_url_pattern.match(url):
                # This is the link you are looking for
                joblink = url
                break

    driver.close()
    driver.quit()
    return joblink
