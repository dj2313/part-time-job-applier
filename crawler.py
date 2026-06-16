from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
from config import USER_AGENT
from logger import logger

def find_target_page(base_url):
    """
    Crawls the base_url to find a job, career, or contact page using Playwright.
    Returns the URL of the most relevant page and its text content.
    """
    keywords = ['job', 'jobs', 'karriere', 'career', 'bewerbung', 'kontakt', 'contact']
    domain = urlparse(base_url).netloc
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=USER_AGENT)
            page = context.new_page()
            
            logger.info(f"Crawling {base_url}...")
            page.goto(base_url, wait_until="domcontentloaded", timeout=15000)
            
            best_link = None
            
            # Extract links
            links = page.eval_on_selector_all("a[href]", "elements => elements.map(e => ({href: e.href, text: e.innerText}))")
            
            for link in links:
                href = link.get("href", "")
                text = (link.get("text") or "").lower()
                
                full_url = urljoin(base_url, href)
                link_domain = urlparse(full_url).netloc
                
                if link_domain == domain:
                    for kw in keywords:
                        if kw in text or kw in href.lower():
                            best_link = full_url
                            if kw in ['job', 'jobs', 'karriere', 'career', 'bewerbung']:
                                break
                    if best_link and any(kw in best_link.lower() for kw in ['job', 'karriere', 'bewerbung']):
                        break
                        
            target_url = best_link if best_link else base_url
            logger.info(f"Target page for {base_url} is {target_url}")
            
            if target_url != base_url:
                page.goto(target_url, wait_until="domcontentloaded", timeout=15000)
                
            # Remove scripts and styles
            page.evaluate("document.querySelectorAll('script, style, nav, footer').forEach(e => e.remove())")
            
            content = page.evaluate("document.body.innerText")
            forms_html = page.evaluate("Array.from(document.querySelectorAll('form')).map(f => f.outerHTML).join('\\n')")
            
            browser.close()
            
            combined_content = f"TEXT CONTENT:\n{content[:5000]}\n\nFORMS HTML:\n{forms_html[:5000]}"
            return target_url, combined_content
            
    except Exception as e:
        logger.error(f"Playwright error crawling {base_url}: {e}")
        return None, None
