import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from config import USER_AGENT

logging.basicConfig(level=logging.INFO)

def find_target_page(base_url):
    """
    Crawls the base_url to find a job, career, or contact page.
    Returns the URL of the most relevant page and its text content.
    """
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to fetch {base_url}: {e}")
        return None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Keywords to look for in links
    keywords = ['job', 'jobs', 'karriere', 'career', 'bewerbung', 'kontakt', 'contact']
    
    best_link = None
    domain = urlparse(base_url).netloc
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        text = a_tag.get_text().lower()
        
        # Resolve relative URLs
        full_url = urljoin(base_url, href)
        link_domain = urlparse(full_url).netloc
        
        if link_domain == domain:
            for kw in keywords:
                if kw in text or kw in href.lower():
                    best_link = full_url
                    # Prioritize job/career over contact
                    if kw in ['job', 'jobs', 'karriere', 'career', 'bewerbung']:
                        break
            if best_link and any(kw in best_link.lower() for kw in ['job', 'karriere', 'bewerbung']):
                break # Found a highly relevant link, stop searching
                
    target_url = best_link if best_link else base_url
    logging.info(f"Target page for {base_url} is {target_url}")
    
    # Fetch content of the target page
    try:
        if target_url != base_url:
            target_response = requests.get(target_url, headers=headers, timeout=10)
            target_response.raise_for_status()
            target_soup = BeautifulSoup(target_response.text, 'html.parser')
        else:
            target_soup = soup
            
        # Extract visible text and forms for the LLM to analyze
        # We'll just pass a somewhat cleaned HTML or text to save tokens
        for script in target_soup(["script", "style", "nav", "footer"]):
            script.decompose()
        content = target_soup.get_text(separator=' ', strip=True)
        # Also grab forms html as string to help with field mapping
        forms_html = "".join([str(f) for f in target_soup.find_all('form')])
        
        combined_content = f"TEXT CONTENT:\n{content[:5000]}\n\nFORMS HTML:\n{forms_html[:5000]}"
        return target_url, combined_content
        
    except Exception as e:
        logging.error(f"Failed to fetch target page {target_url}: {e}")
        return None, None
