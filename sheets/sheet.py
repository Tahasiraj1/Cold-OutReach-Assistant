import gspread

class GoogleSheets:
    def __init__(self):
        self.client = gspread.service_account(filename="credentials_sheets.json")
        self.sheet = self.client.open('potential clients 118 business').sheet1

    def get_existing_rows(self):
        rows = self.sheet.get_all_values()
        return rows[1:]  # Skip header

    def get_pending_reach_rows(self):
        """
        Returns list of dicts for rows where 'Reach' is empty and Email exists.
        """
        rows = self.get_existing_rows()
        pending = []

        for i, row in enumerate(rows):
            try:
                company = row[0].strip() if len(row) > 0 else ''
                address = row[1].strip() if len(row) > 1 else ''
                company_details = row[2].strip() if len(row) > 2 else ''
                website = row[3].strip() if len(row) > 3 else ''
                email = row[4].strip() if len(row) > 4 else ''
                category = row[5].strip() if len(row) > 5 else ''
                phone = row[6].strip() if len(row) > 6 else ''
                reach = row[7].strip() if len(row) > 7 else ''
                follow_up = row[8].strip() if len(row) > 8 else ''

                if email and not reach:
                    pending.append({
                        'row_index': i + 2,  # +2 to account for header + 0-indexing
                        'company': company,
                        'address': address,
                        'company_details': company_details,
                        'website': website,
                        'email': email,
                        'category': category,
                        'phone': phone,
                        'reach': reach,
                        'follow_up': follow_up
                    })
            except Exception as e:
                print(f"Error processing row {i + 2}: {e}")
                continue

        return pending

    def mark_reach_done(self, row_index):
        self.sheet.update_cell(row_index, 8, 'Done')  # Reach = H = col 8

    def mark_followup_done(self, row_index):
        self.sheet.update_cell(row_index, 9, 'Done')  # Follow up = I = col 9


if __name__ == "__main__":
    gs = GoogleSheets()
    leads = gs.get_pending_reach_rows()

    count = 1
    for lead in leads:
        print(f"{lead['company']} - {lead['email']} - {lead['company_details']}\n\n")
        count += 1
        if count == 5:
            break

