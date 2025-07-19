from .instructions import OUTREACH_AGENT_INSTRUCTIONS
from tools.outreach_pipeline import outreach_pipeline
from utils.get_gemini_model import get_gemini_model
from agents import Agent

model = get_gemini_model()

email_assistant = Agent(
    name="Email Assistant",
    instructions=f"{OUTREACH_AGENT_INSTRUCTIONS}",
    model=model,
    tools=[outreach_pipeline],
)