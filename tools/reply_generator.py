from .summarize import summarize_email
import google.generativeai as genai
from pydantic import EmailStr
from email_modules.fetcher import EmailFetcher
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

def generate_email_content(email: EmailStr, summary: str, user_query: str = None) -> str:
    """
    Generate a cold outreach email draft based on lead info and context.
    """
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

    # Cold outreach-specific system prompt
    prompt = (
        "You are a cold outreach assistant working on behalf of Taha Siraj.\n"
        "Taha helps small businesses improve their websites (speed, design, SEO) and build online presence.\n"
        "You're sending first-contact emails to business owners who may not know him yet.\n\n"
        "🚫 DO NOT:\n"
        "- Say 'Here's your email', 'Here's the draft', or add commentary.\n"
        "- Add placeholders like [Your Name], [Recipient], [Your Company], etc.\n"
        "- Be overly polite or robotic. No marketing fluff.\n\n"
        "✅ DO:\n"
        "- Keep it personal, clear, and sound like a real person is emailing.\n"
        "- Make the message sound like it was written one-on-one.\n"
        "- Mention clear value points like performance, SEO, or poor mobile experience.\n"
        "- Offer a free audit or brief call if it fits the tone.\n"
        "- Link to Taha’s real-world portfolio if appropriate.\n"
    )

    if user_query:
        prompt += f"""\n🧠 Lead Context or Business Type:
        {user_query}

        ✉️ Now, write a personalized cold email that:
        - Reflects this business's likely pain points.
        - Offers a solution or insight in plain language.
        - Signs off with Taha Siraj.
        """
    elif email and summary:
        prompt += f"""\n🧠 Lead Info:
        {summary}

        ✉️ Now, write a short cold outreach email that:
        - Shows you reviewed their business/site (based on the summary).
        - Gently points out what can be improved (speed, mobile, design, etc.).
        - Offers to help or provide a free audit.
        - Signs off with Taha Siraj.
        """
    else:
        raise ValueError("Insufficient input: Provide either user_query or both email and summary.")

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Error generating email content: {e}")


if __name__ == "__main__":
    fether = EmailFetcher()
    email = fether.fetch_emails()
    print(email)
    summary = summarize_email(email)
    reply = generate_email_content(email=email, summary=summary)
    print(reply)