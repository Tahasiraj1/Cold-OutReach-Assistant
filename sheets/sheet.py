import gspread

class GoogleSheets:
    def __init__(self):
        self.client = gspread.service_account(filename="credentials.json")
        self.sheet = self.client.open('potential clients 118 business').sheet1

    def get_existing_rows(self):
        rows = self.sheet.get_all_values()
        return rows[1:]  # Skip header
    
    def get_emails(self):
        rows = self.get_existing_rows()
        emails = set()
        for row in rows:
            emails.add(row[6])
        return emails
    
    def get_company_detials(self):
        rows = self.get_existing_rows()
        company_details = set()
        for row in rows:
            company_details.add(row[2])
        return company_details
    
if __name__ == "__main__":
    sheet = GoogleSheets()
    print(sheet.get_emails())