import imaplib
import email
import re
from html import unescape

# Email server configuration
server_name = "outlook.office365.com"
port = 993  # Port for TLS (IMAPS)

# Connect to the server
mail = imaplib.IMAP4_SSL(server_name, port)  # Use IMAP4_SSL for TLS encryption

# Log in to your email account
username = "hrvatar@outlook.com"
password = "@hassansana1"
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

# Print the verification links
for link in verification_links:
    print("Verification Link:", link)
# print("\nEmail Subject:", email_subject)
# print("\nEmail Body:")
# print(email_body)

# Close the connection
mail.logout()
