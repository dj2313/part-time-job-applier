import json
import time
from pathlib import Path

from config import PROFILE_PATH, APPLIED_PATH, DELAY_BETWEEN_SITES, MAX_APPLICATIONS_PER_RUN
from logger import logger
from discovery import discover_places
from crawler import find_target_page
from decision import decide_application_method
from cover_letter import generate_cover_letter
from apply_form import fill_and_submit_form
from apply_email import send_application_email
from notifier import send_telegram_message

def load_profile():
    if not PROFILE_PATH.exists():
        logger.error(f"Profile file not found at {PROFILE_PATH}")
        return {}
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_applied():
    if not APPLIED_PATH.exists():
        return []
    with open(APPLIED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_applied(applied_list):
    with open(APPLIED_PATH, "w", encoding="utf-8") as f:
        json.dump(applied_list, f, indent=4)

def main():
    try:
        profile = load_profile()
        if not profile:
            return
            
        applied_urls = load_applied()
        
        logger.info("Starting Minijob Agent Pipeline...")
        send_telegram_message("🤖 Minijob Agent Pipeline started!")
        
        # 1. Discover places
        places = discover_places()
        if not places:
            logger.warning("No places found.")
            return
            
        successful_applications = 0
            
        for place in places:
            if successful_applications >= MAX_APPLICATIONS_PER_RUN:
                logger.info(f"Reached MAX_APPLICATIONS_PER_RUN ({MAX_APPLICATIONS_PER_RUN}). Stopping for now.")
                break
                
            base_url = place["website"]
            place_name = place["name"]
            
            if base_url in applied_urls:
                logger.info(f"Already applied/processed {base_url}. Skipping.")
                continue
                
            logger.info(f"--- Processing {place_name} ({base_url}) ---")
            
            # Respect delay between sites
            time.sleep(DELAY_BETWEEN_SITES)
            
            # 2. Crawl to find target page
            target_url, content = find_target_page(base_url)
            if not target_url or not content:
                logger.warning(f"Could not extract content from {base_url}. Marking as processed.")
                applied_urls.append(base_url)
                save_applied(applied_urls)
                continue
                
            # 3. Decide method
            decision = decide_application_method(target_url, content)
            if not decision:
                logger.warning(f"Could not make a decision for {target_url}. Marking as processed.")
                applied_urls.append(base_url)
                save_applied(applied_urls)
                continue
                
            method = decision.get("method")
            
            # 4. Generate cover letter
            message = generate_cover_letter(place_name, profile)
            
            success = False
            attempt_details = f"Target: {place_name}\nURL: {target_url}\nMethod: {method}"
            
            # 5. Apply
            if method == "email" and decision.get("email"):
                target_email = decision["email"]
                subject = f"Bewerbung als Minijobber - {profile.get('full_name')}"
                success = send_application_email(target_email, subject, message, profile.get("cv_path"))
                attempt_details += f"\nEmail: {target_email}"
                
            elif method == "form":
                success = fill_and_submit_form(target_url, decision, profile, message)
                
            else:
                logger.warning(f"Unknown or invalid method '{method}' or missing email for {target_url}")
                
            # 6. Notify and track
            if success:
                logger.info(f"Successfully applied to {place_name}!")
                send_telegram_message(f"✅ <b>Application sent!</b>\n{attempt_details}")
                successful_applications += 1
            else:
                logger.error(f"Failed to apply to {place_name}.")
                send_telegram_message(f"❌ <b>Application failed.</b>\n{attempt_details}")
                
            # Add to applied list regardless to avoid retrying failed forms endlessly
            applied_urls.append(base_url)
            save_applied(applied_urls)
            
        logger.info("Pipeline finished.")
        send_telegram_message(f"🏁 Minijob Agent Pipeline finished. Total successful: {successful_applications}")

    except Exception as e:
        logger.exception(f"Unhandled exception in pipeline: {e}")
        send_telegram_message(f"🚨 <b>Pipeline crashed with an error:</b>\n{e}")

if __name__ == "__main__":
    main()

