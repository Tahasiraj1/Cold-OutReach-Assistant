from sheets.sheet import GoogleSheets
from email_modules.composer import NewEmailManager
from tools.reply_generator import generate_email_content
from agents import function_tool
import chainlit as cl

async def send():
    pass

@function_tool
async def outreach_pipeline(subject: str, body: str):
    """
        Sends an email to the lead with the subject and body extracted from the pitch.

        Args:
            subject (str): The subject line of the email. (Extract from pitch)
            body (str): The body of the email. (Extract from pitch)
    """
    gs = GoogleSheets()
    leads = gs.get_pending_reach_rows()

    if not leads:
        await cl.Message(content="✅ No pending leads found in Google Sheets.").send()
        return

    for lead in leads:
        try:
            await cl.Message(content=f"📋 Processing lead: {lead['company']} ({lead['email']})").send()
            user_query = (
                f"Business: {lead['company']}\n"
                f"Details: {lead['company_details']}\n"
                f"Website: {lead['website']}"
            )

            pitch = generate_email_content(
                details=lead['company_details'],
                user_query=user_query
            )

            manager = NewEmailManager(
                to=lead['email'],
                subject=pitch['subject'],
                body=lead['body']
            )
            
            manager.draft()
            gs.mark_reach_done(lead['row_index'])
            await cl.Message(content=f"✅ Email sent to {lead['email']} and marked as reached.").send()
        except Exception as e:
            await cl.Message(content=f"❌ Failed to process lead {lead['email']}: {e}").send()
    await cl.Message(content="🎉 Finished processing all leads.").send()
