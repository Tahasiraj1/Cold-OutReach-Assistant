from .instructions import COMPOSER_INSTRUCTIONS, EMAIL_ASSISTANT_INSTRUCTIONS, DRAFTER_INSTRUCTIONS
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from tools.process_pipeline import process_emails_pipeline
from tools.compose_pipeline import compose_email_pipeline
from tools.draft_pipeline import draft_new_email_pipeline
from tools.draft_pipeline import draft_new_email_pipeline
from utils.get_gemini_model import get_gemini_model
from agents import Agent

model = get_gemini_model()

drafter_agent = Agent(
    name="Drafter Agent",
    instructions=DRAFTER_INSTRUCTIONS,
    handoff_description='You are a professional Email Drafter tasked with automating Gmail inbox management. Your objective is to efficiently draft new emails using the draft_new_email_pipeline function.',
    model=model,
    tools=[draft_new_email_pipeline],
)

composer_agent = Agent(
    name="Composer Agent",
    instructions=COMPOSER_INSTRUCTIONS,
    handoff_description='You are a professional Email Composer tasked with automating Gmail inbox management. Your objective is to efficiently compose emails using the compose_email_pipeline function.',
    model=model,
    tools=[compose_email_pipeline],
)

email_assistant = Agent(
    name="Email Assistant",
    instructions=f"{RECOMMENDED_PROMPT_PREFIX}\n\n{EMAIL_ASSISTANT_INSTRUCTIONS}",
    model=model,
    tools=[process_emails_pipeline],
    handoffs=[composer_agent, drafter_agent],
)