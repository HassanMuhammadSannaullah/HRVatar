import time
import imaplib
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import email  # Import email module for email parsing
from html import unescape


def PostJob(title, skills, Description, Country, State=None):
    # Initialize the WebDriver with WebDriverManager
    driver = webdriver.Chrome(
        service=Service(executable_path=ChromeDriverManager().install())
    )

    username = "hrvatar@outlook.com"
    password = "@hassansana1"
    joblink = ""
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

    time.sleep(10)
    # Email server configuration
    server_name = "outlook.office365.com"
    port = 993  # Port for TLS (IMAPS)

    # Connect to the server
    mail = imaplib.IMAP4_SSL(server_name, port)  # Use IMAP4_SSL for TLS encryption

    # Log in to your email account

    mail.login(username, password)

    # Select the mailbox you want to search
    mailbox_name = "INBOX"
    mail.select(mailbox_name)

    # Search for all email IDs in the mailbox
    status, email_ids = mail.search(None, "ALL")

    # Get the latest email ID
    latest_email_id = email_ids[0].split()[-1]

    # Fetch the latest email by ID
    status, email_data = mail.fetch(latest_email_id, "(RFC822)")

    # Parse the email content
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # # Function to recursively find verification link in email content
    # def find_verification_link(message):
    #     for part in message.walk():
    #         if part.get_content_type() == "text/html":
    #             body = part.get_payload(decode=True).decode()
    #             links = re.findall(r'href=["\'](https?://[^"\']+)["\']', body)
    #             for link in links:
    #                 if "verification" in link:
    #                     return link
    #     return None

    # verification_link = find_verification_link(email_message)

    # if verification_link:
    #     print("Verification Link found:", verification_link)
    # else:
    #     print("No verification link found in the latest email.")

    # Print the email subject and body
    email_subject = email_message.get("Subject")
    email_body = email_message.get_payload(decode=True).decode()

    # Define a regular expression pattern to match URLs containing "serviceFreeJobActivate"
    url_pattern = r'https?://[^\s<>"]*serviceFreeJobActivate[^\s<>"]*'

    # Use re.findall to extract all matching URLs from the email body
    verification_links = re.findall(url_pattern, unescape(email_body))

    mail.logout()

    driver.close()
    driver.quit()

    return verification_links[-1]


if __name__ == "__main__":
    print(PostJob("test", "test", "test", "Oman"))
