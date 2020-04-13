import requests
import re

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }

# previously findGA
def scrapeMatch(domain: str) -> tuple:
    # Find tracking ids, returns a tuple of lists; currently analytics ids and adsense ids 
    print(f"Scraping {domain} for Google Analytics and Adsense ids...")
    p = re.compile(r"(UA-[0-9]+-[0-9]+)|(pub-\d{16})", re.IGNORECASE) 
    page = requests.get(domain, headers=headers).text
    results = p.findall(page)
    ga_ids = []
    gadsense_ids = []
    for match in results:
        if match[0]:
            if match[0][-2] == "-":
                ga_id = match[0][0:-2]
                print(f"Found {ga_id}")
                ga_ids.append(ga_id)
        if match[1]: 
            print(f"Found {match[1]}")
            gadsense_ids.append(match[1])
    return list(set(ga_ids)), list(set(gadsense_ids))

