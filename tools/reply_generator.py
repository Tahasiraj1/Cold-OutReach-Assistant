import google.generativeai as genai
from dotenv import load_dotenv
import ast
import os
import re

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")


def generate_email_content(
    details: str = None,
    user_query: str = None,
) -> str:
    """
    Generate a cold outreach email draft based on lead info, tone, and business context.
    """

    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

    prompt = (
        f"You are a cold outreach assistant working on behalf of Taha Siraj.\n"
        f"Taha helps small businesses improve their websites (speed, mobile UX, SEO).\n"
        f"You are writing cold emails to business owners who have never heard of him.\n\n"
        "ALWAYS return a python dictionary with the following keys:\n"
        "- 'subject': The subject line of the email.\n"
        "- 'body': The body of the email.\n"

        f"🎯 OBJECTIVE:\n"
        f"Write a short, personalized email that:\n"
        f"- Hooks attention early by showing relevance.\n"
        f"- Identifies 1–2 pain points (slow site, bad SEO, not mobile-friendly).\n"
        f"- Offers a free website audit or short call.\n"
        f"- Signs off as Taha Siraj with contact details.\n\n"

        f"- Casual: relaxed, friendly, low pressure.\n"
        f"- Confident: assertive, expert-driven, value-forward.\n"
        f"- Persuasive: results-oriented, focused on urgency and missed opportunity.\n"
        f"- Professional: clean, respectful, minimal flair.\n\n"

        f"🚫 DO NOT:\n"
        f"- Use fluff or marketing buzzwords.\n"
        f"- Add 'Here's your draft' or placeholders.\n\n"

        f"✅ ALWAYS:\n"
        f"- Mention Taha's name and value.\n"
        f"- Use natural, 1-on-1 tone.\n"
        f"- Close with contact info:\n"
        f"    Portfolio: https://my-portfolio-eta-one-97.vercel.app/\n"
        f"    LinkedIn: https://www.linkedin.com/in/taha-siraj-521b512b7/\n"
        f"    Email: tahasiraj242@gmail.com\n"
        f"    Phone: +92 3311245238\n"
    )

    if user_query and details:
        prompt += f"""\n🧠 Lead Profile:
        - Business Type or Query: {user_query}
        - Website Details or Observations: {details}

        ✉️ Write a cold email that combines both business context and technical insights. Address likely pain points based on the query and details, show how Taha can help, and end with a clear call to action.
        """
    elif user_query:
        prompt += f"""\n🧠 Lead Business Type or Query:
        {user_query}

        ✉️ Write a cold email reflecting this business's likely problems (UX, SEO, tech), explain how Taha can help, and invite them to respond.
        """
    elif details:
        prompt += f"""\n🧠 Lead Website Observations:
        {details}

        ✉️ Write a concise, technical cold email highlighting weaknesses (site speed, UX, SEO), offer a free audit, and end with contact info.
        """
    else:
        raise ValueError("Either 'user_query', 'details', or both must be provided.")


    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Remove markdown code block markers (```python, ```, etc.)
        text = re.sub(r"^```(?:python)?\s*|```$", "", text, flags=re.MULTILINE).strip()

        # Parse the dictionary safely
        result = ast.literal_eval(text)
        subject = result.get("subject", "")
        body = result.get("body", "")
        if not subject or not body:
            raise ValueError("Missing subject or body in Gemini output.")
        return {"subject": subject, "body": body}
    except Exception as e:
        raise Exception(f"Error generating email content: {e}")

if __name__ == "__main__":
    print(generate_email_content(details="24/7 North East Plumbing and Drainage Immediate response. We respond 24/7 to emergency plumbing and drainage needs. Just call 07935202607. We repair and maintain all plumbing and drainage needs in the North East."))
