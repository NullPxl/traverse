import requests
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }

def scrapeMatch(domain: str) -> dict:
    # Find tracking ids, returns a dict of lists; currently analytics ids and adsense ids 
    print(f"Scraping {domain} for Google Analytics and Adsense ids...")
    p = re.compile(r"(UA-[0-9]+-[0-9]+)|(pub-\d{16})", re.IGNORECASE) 
    page = requests.get(domain, headers=headers).text
    results = p.findall(page)
    ids = {"analytics": [], "adsense": []}
    for match in results:
        if match[0]:
            if match[0][-2] == "-":
                ga_id = match[0][0:-2]
                ids["analytics"].append(ga_id)
                print(f"\t Found: {ga_id}")
        if match[1]: # adsense id
            ids["adsense"].append(match[1])
            print(f"\tFound: {match[1]}")

    return ids # {'analytics': ['UA-123456'], 'adsense': ["pub-217321213123..."]}

