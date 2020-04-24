import requests
import re
from .conf import bcolors

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }

def scrapeMatch(domain: str) -> dict:
    # Find tracking ids, returns a dict of lists; currently analytics ids and adsense ids 
    print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Scraping {domain} for Google Analytics and Adsense ids...")
    ids = {"analytics": [], "adsense": []}
    p = re.compile(r"(UA-[0-9]+-[0-9]+)|(pub-\d{16})", re.IGNORECASE)
    try: 
        page = requests.get(domain, headers=headers).text
    except:
        print(f"{bcolors.FAIL}[X]{bcolors.ENDC} ERROR making a request to: \"{domain}\"")
        return ids
    results = p.findall(page)
    for match in results:
        if match[0]:
            if match[0][-2] == "-":
                ga_id = match[0][0:-2]
                ids["analytics"].append(ga_id)
                print(f"  > Found: {ga_id}")
        if match[1]: # adsense id
            ids["adsense"].append(match[1])
            print(f"  > Found: {match[1]}")

    return ids # {'analytics': ['UA-123456'], 'adsense': ["pub-217321213123..."]}

