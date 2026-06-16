import requests
import json
from config import BBOX, AMENITIES, OVERPASS_URL, PLACES_PATH
from logger import logger
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def discover_places():
    """
    Query Overpass API for places matching the criteria.
    """
    logger.info(f"Discovering places with amenities: {AMENITIES}")
    
    # Construct Overpass QL query
    amenity_filter = "|".join(AMENITIES)
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"~"{amenity_filter}"]["website"]({BBOX});
      way["amenity"~"{amenity_filter}"]["website"]({BBOX});
      relation["amenity"~"{amenity_filter}"]["website"]({BBOX});
    );
    out center;
    """
    
    try:
        response = requests.post(OVERPASS_URL, data={'data': query})
        response.raise_for_status()
        data = response.json()
        
        places = []
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            place = {
                "id": element.get("id"),
                "name": tags.get("name", "Unknown"),
                "website": tags.get("website"),
                "amenity": tags.get("amenity"),
                "lat": element.get("lat") or element.get("center", {}).get("lat"),
                "lon": element.get("lon") or element.get("center", {}).get("lon")
            }
            if place["website"]:
                # Basic URL cleanup
                if not place["website"].startswith("http"):
                    place["website"] = "http://" + place["website"]
                places.append(place)
                
        # Save to places.json
        with open(PLACES_PATH, "w", encoding="utf-8") as f:
            json.dump(places, f, indent=4, ensure_ascii=False)
            
        logger.info(f"Found {len(places)} places with websites. Saved to {PLACES_PATH}")
        return places
        
    except Exception as e:
        logger.error(f"Failed to query Overpass API: {e}")
        raise # Reraise for tenacity

if __name__ == "__main__":
    discover_places()
