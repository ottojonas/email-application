import requests
from icecream import ic

from auth import get_access_token

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


def send_email(recipient, subject, body):
    access_token = get_access_token()
    url = f"{GRAPH_API_ENDPOINT}/me/sendMail"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        },
        "saveToSentItems": "true",
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 202:
        ic("email sent successfully")
    else:
        ic(f"error sending email: {response.status_code}, {response.text}")


def get_inbox_emails():
    access_token = get_access_token()
    url = f"{GRAPH_API_ENDPOINT}/me/messages"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        emails = response.json().get("value", [])
        for email in emails:
            ic(f"From: {email['from']['emailAddress']['address']}")
            ic(f"Subject: {email['subject']}")
            ic(f"Body: {email['bodyPreview']}")
            ic("-" * 40)
    else:
        ic(f"Error fetching emails: {response.status_code}, {response.text}")


if __name__ == "__main__":
    send_email(
        "ottobjonas03@outlook.com",
        "test email",
        "this is a test email from an email client i developed",
    )
    get_inbox_emails()
