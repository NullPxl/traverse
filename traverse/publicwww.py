import api_keys
import urllib.parse
import requests
from time import sleep
from .conf import bcolors

# Free version of PublicWWW only allows for the top 3,000,000 sites in results (Most popular of 535M pages)
# Paid versions allow for their entire dataset, but it's $49/m or $490/y

class PublicWWW:

    def __init__(self, token: str, queries: list):
        self.queries = [urllib.parse.quote(query) for query in queries]

    def getDatafromQuery(self) -> list:
        pwww_url = f"https://publicwww.com/websites/\"THE_QUERY\"/?export=urls&key={api_keys.publicwww}"
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
                }
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying PublicWWW...")
        
        info = {}
        for q in self.queries:
            # if len(self.queries) > 2 and q == self.queries[-1]:
            #     # publicwww has rate limiting on what appears to be the api keys for consecutive reqs
            #     # need to get a better way to do this (rotating ips not working :( ))
            #     print("Due to rate limiting with more than 2 queries, waiting for 60 seconds before making next request (it may take longer")
            #     sleep(60.0)

            r = requests.get(pwww_url.replace("THE_QUERY", q), headers=headers)
            uq_q = urllib.parse.unquote(str(q))
            data = r.text
            if data == "Wrong API key":
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} Invalid PublicWWW API Key provided.")
                return []
            else:
                info[uq_q] = [url for url in data.split("\n") if url]
                print(f"  - {uq_q}: {len(info[uq_q])} results")
        results = []
        for l in info.values():
            results.extend(l)
        return results
