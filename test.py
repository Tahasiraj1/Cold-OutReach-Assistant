from tools.reply_generator import generate_email_content
from sheets.sheet import GoogleSheets

def test_generate_email_content():
    sheet = GoogleSheets()
    email = sheet.get_emails()
    summary = sheet.get_company_detials()
    reply = generate_email_content(email=list(email)[0], summary=list(summary)[0])
    print(reply)

if __name__ == "__main__":
    pitch = test_generate_email_content()
    print(pitch)