import os
import json
import logging
from groq import Groq
from config import GROQ_API_KEY

logging.basicConfig(level=logging.INFO)

def decide_application_method(url, content):
    """
    Uses Groq API to decide if we should use an email or a form.
    Returns a strict JSON format.
    """
    if not GROQ_API_KEY:
        logging.error("GROQ_API_KEY is missing.")
        return None

    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
    Analyze the following content from a cafe/restaurant website ({url}).
    Determine the best way to apply for a part-time job (minijob).
    
    Is there an application form, or just a contact email address?
    
    Output strictly in JSON format matching this schema:
    {{
        "method": "email" or "form",
        "email": "the email address found, or null",
        "form_action": "the form action URL if method is form, or null",
        "fields": {{
            "name": "selector for name field, or null",
            "email": "selector for email field, or null",
            "phone": "selector for phone field, or null",
            "message": "selector for message field, or null",
            "cv": "selector for CV upload field, or null"
        }},
        "submit_hint": "css selector for the submit button, or null"
    }}
    
    Content to analyze:
    {content[:8000]}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a web parsing assistant. Output ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-70b-8192",
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        result_str = chat_completion.choices[0].message.content
        result_json = json.loads(result_str)
        return result_json
        
    except Exception as e:
        logging.error(f"Groq API error during decision: {e}")
        return None
