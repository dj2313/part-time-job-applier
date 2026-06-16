import logging
import time
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO)

def fill_and_submit_form(url, decision_data, profile, message):
    """
    Uses Playwright to fill out and submit the application form.
    Returns True if successful, False otherwise.
    """
    fields = decision_data.get("fields", {})
    submit_hint = decision_data.get("submit_hint")
    
    if not any(fields.values()):
        logging.warning(f"No fields found to fill on {url}.")
        return False
        
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            logging.info(f"Navigating to {url} for form submission...")
            page.goto(url, wait_until="networkidle", timeout=15000)
            
            # Fill out the form
            if fields.get("name") and page.locator(fields["name"]).count() > 0:
                page.fill(fields["name"], profile.get("full_name", ""))
            
            if fields.get("email") and page.locator(fields["email"]).count() > 0:
                page.fill(fields["email"], profile.get("email", ""))
                
            if fields.get("phone") and page.locator(fields["phone"]).count() > 0:
                page.fill(fields["phone"], profile.get("phone", ""))
                
            if fields.get("message") and page.locator(fields["message"]).count() > 0:
                page.fill(fields["message"], message)
                
            if fields.get("cv") and page.locator(fields["cv"]).count() > 0:
                cv_path = profile.get("cv_path")
                if cv_path:
                    page.locator(fields["cv"]).set_input_files(cv_path)
            
            # Take a screenshot before submit (optional, good for debugging)
            # page.screenshot(path="before_submit.png")
            
            # Try to submit
            if submit_hint and page.locator(submit_hint).count() > 0:
                logging.info(f"Clicking submit button: {submit_hint}")
                page.click(submit_hint)
                time.sleep(2) # Wait a bit for submission to process
                logging.info("Form submitted successfully via known button.")
                browser.close()
                return True
            else:
                # Fallback: try to find any submit button in the form
                submit_buttons = page.locator('button[type="submit"], input[type="submit"]')
                if submit_buttons.count() > 0:
                    submit_buttons.first.click()
                    time.sleep(2)
                    logging.info("Form submitted successfully via fallback button.")
                    browser.close()
                    return True
                else:
                    logging.warning("Could not find a submit button.")
                    browser.close()
                    return False
                    
    except Exception as e:
        logging.error(f"Playwright error filling form on {url}: {e}")
        return False
