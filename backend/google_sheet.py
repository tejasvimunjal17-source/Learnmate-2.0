import requests
from config import CONFIG


def save_user(first_name, last_name, email):
    """Save registration data to Google Sheets."""

    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email_address,
    }

    try:
        response = requests.post(
            CONFIG.google_sheet_url,
            json=data,
            timeout=10,
        )

        return response.status_code == 200

    except Exception as e:
        print("Google Sheet Error:", e)
        return False
