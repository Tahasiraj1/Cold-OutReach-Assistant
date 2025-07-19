from tools.reply_generator import generate_email_content
from email_modules.composer import NewEmailManager
from sheets.sheet import GoogleSheets
from agents import function_tool
import chainlit as cl
import asyncio

@function_tool
async def outreach_pipeline():
    gs = GoogleSheets()
    leads = gs.get_pending_reach_rows()

    if not leads:
        await cl.Message(content="✅ No pending leads found in Google Sheets.").send()
        return

    for lead in leads:
        try:
            await cl.Message(content=f"📋 Processing lead: {lead['company']} ({lead['email']})").send()
            details = (
                f"Business: {lead['company']}\n"
                f"Details: {lead['company_details']}\n"
                f"Website: {lead['website']}"
                f"Category: {lead['category']}"
            )

            pitch = generate_email_content(details=details)

            manager = NewEmailManager(
                to=lead['email'],
                subject=pitch['subject'],
                body=pitch['body']
            )

            manager.compose_email()
            gs.mark_reach_done(lead['row_index'])
            await cl.Message(content=f"✅ Email sent to {lead['email']} and marked as reached.").send()
            await asyncio.sleep(60)
        except Exception as e:
            await cl.Message(content=f"❌ Failed to process lead {lead['email']}: {e}").send()
    await cl.Message(content="🎉 Finished processing all leads.").send()
