import requests
import re
from .conf import bcolors

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }

def matcher(page, ids) -> dict:
    # Find tracking ids, returns a dict of lists; currently analytics ids and adsense ids 
    # print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Scraping {domain} for Google Analytics and Adsense ids...")
    p = re.compile(r"(UA-[0-9]+-[0-9]+)|(pub-\d{16})", re.IGNORECASE)
    results = p.findall(page)
    for match in results:
        if match[0]:
            if match[0][-2] == "-":
                ga_id = match[0][0:-2]
                if ga_id not in ids["analytics"]:
                    ids["analytics"].append(ga_id)
                    print(f"  > Found: {ga_id}")
        if match[1]: # adsense id
            if match[1] not in ids["adsense"]:
                ids["adsense"].append(match[1])
                print(f"  > Found: {match[1]}")
    return ids # {'analytics': ['UA-123456'], 'adsense': ["pub-217321213123..."]}

def scrapeMatch(domain: str) -> dict:
    ids = {"analytics": [], "adsense": []}
    # Find tracking ids, returns a dict of lists; currently analytics ids and adsense ids 
    print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Scraping {domain} for Google Analytics and Adsense ids...")
    try: 
        page = requests.get(domain, headers=headers).text
    except:
        print(f"{bcolors.FAIL}[X]{bcolors.ENDC} ERROR making a request to: \"{domain}\"")
        return ids
    ids = matcher(page, ids)
    if not ids["analytics"] and not ids["adsense"]:
        print(f"{bcolors.WARNING}[/]{bcolors.ENDC} No matches were found.")
    return ids

