import re

def clean_text(text: str) -> str:
    text = str(text).lower()

    replacements = {
        "log in": "login",
        "sign in": "login",
        "sign-in": "login",
        "logged in": "login",
        "multi factor authentication": "mfa",
        "multi-factor authentication": "mfa",
        "users": "user",
        "employees": "employee",
        "servers": "server",
        "services": "service",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"http\\S+|www\\S+", " ", text)
    text = re.sub(r"\\b\\d{1,3}(?:\\.\\d{1,3}){3}\\b", " IPADDRESS ", text)
    text = re.sub(r"[^a-zA-Z\\s]", " ", text)
    text = re.sub(r"\\s+", " ", text).strip()

    return text
