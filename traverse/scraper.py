import requests
import re
import datetime
from .conf import bcolors


def getArchiveTimestamp(url) -> str:
    # For ids found in an archived url, it can be helpful to see the date it appeared on
    timestamp = ""
    if "web.archive.org/web/" in url:
        try:
            ts = url.split("web/")[1].split("/")[0]
            d = datetime.datetime.strptime(ts, "%Y%m%d%H%M%S")
            timestamp = f"{d.strftime('%b %d, %Y')} ({ts})"
        except:
            pass
    return timestamp

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }

def matcher(page, ids, domain) -> dict:
    # Find tracking ids, returns a dict of lists; currently analytics ids and adsense ids 
    p = re.compile(r"(UA-[0-9]+-[0-9]+)|(pub-\d{16})", re.IGNORECASE)
    results = p.findall(page)
    for match in results:
        if match[0]: # analytics id
            if match[0][-2] == "-":
                ga_id = match[0][0:-2]
                if ga_id not in ids["analytics"]:
                    ids["analytics"].append(ga_id)
                    print(f"  > [Google Analytics]: {ga_id} {getArchiveTimestamp(domain)}")
        if match[1]: # adsense id
            if match[1] not in ids["adsense"]:
                ids["adsense"].append(match[1])
                print(f"  > [Google Adsense]: {match[1]} {getArchiveTimestamp(domain)}")
        
    return ids # {'analytics': ['UA-123456'], 'adsense': ["pub-217321213123..."]}

def scrapeMatch(domain: str) -> dict:
    # Scrape the live webpage and return the found ids
    ids = {"analytics": [], "adsense": []}
    print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Scraping {domain} for Google Analytics and Adsense ids...")
    try: 
        page = requests.get(domain, headers=headers).text
    except:
        print(f"{bcolors.FAIL}[X]{bcolors.ENDC} ERROR making a request to: \"{domain}\"")
        return ids
    ids = matcher(page, ids, domain)
    if not ids["analytics"] and not ids["adsense"]:
        print(f"{bcolors.WARNING}[/]{bcolors.ENDC} No matches were found.")
    return ids

