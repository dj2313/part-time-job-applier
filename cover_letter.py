import logging
from groq import Groq
from config import GROQ_API_KEY

logging.basicConfig(level=logging.INFO)

def generate_cover_letter(place_name, profile):
    """
    Generates a short, personalized German A2-level application message via Groq.
    """
    if not GROQ_API_KEY:
        logging.error("GROQ_API_KEY is missing.")
        return "Guten Tag, ich interessiere mich für einen Minijob in Ihrem Team. Mein Lebenslauf ist beigefügt. Mit freundlichen Grüßen."

    client = Groq(api_key=GROQ_API_KEY)
    
    positions_str = ", ".join(profile.get("positions", []))
    
    prompt = f"""
    Write a short, friendly, German A2-level email/message applying for a part-time job (Minijob) at a place called "{place_name}".
    My name is {profile.get("full_name")}.
    I am looking to work as: {positions_str}.
    My availability: {profile.get("availability")}.
    Extra info: {profile.get("extra_info")}.
    
    The message should be no more than 4-5 sentences.
    Keep the language very simple (A2 level), polite, and natural.
    Mention that my CV is attached.
    Do not include any placeholder text like [Your Name] – use the actual provided information.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant writing simple German application messages."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",
            temperature=0.3
        )
        
        return chat_completion.choices[0].message.content.strip()
        
    except Exception as e:
        logging.error(f"Groq API error during cover letter generation: {e}")
        return "Guten Tag, ich bewerbe mich hiermit um einen Minijob. Anbei finden Sie meinen Lebenslauf. Ich freue mich auf Ihre Rückmeldung. Viele Grüße, " + profile.get("full_name", "")
