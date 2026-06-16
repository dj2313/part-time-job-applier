import smtplib
from email.message import EmailMessage
from tenacity import retry, stop_after_attempt, wait_exponential
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD
from logger import logger

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def send_application_email(target_email, subject, message_body, cv_path=None):
    """
    Sends an email using Gmail SMTP.
    Returns True if successful, False otherwise.
    """
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        logging.error("Gmail credentials are not configured.")
        return False
        
    try:
        msg = EmailMessage()
        msg.set_content(message_body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_ADDRESS
        msg['To'] = target_email
        
        # Attach CV if provided
        if cv_path:
            try:
                with open(cv_path, 'rb') as f:
                    pdf_data = f.read()
                msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='CV.pdf')
            except FileNotFoundError:
                logging.error(f"CV file not found at {cv_path}")
                # We can still send the email without it, or choose to fail. Let's send anyway.
            except Exception as e:
                logging.error(f"Error attaching CV: {e}")
                
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
            
        logging.info(f"Successfully sent application email to {target_email}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send email to {target_email}: {e}")
        raise
