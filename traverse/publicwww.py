import urllib.parse
import requests
from time import sleep
from .conf import bcolors

# Free version of PublicWWW only allows for the top 3,000,000 sites in results (Most popular of 535M pages)
# Paid versions allow for their entire dataset, but it's $49/m or $490/y

class PublicWWW:

    def __init__(self, token: str):
        self.token = token

    def getDatafromQuery(self, queries: list) -> list:
        # Return domains that publicwww has indexed to have the supplied string
        if not self.token: 
            print(f"{bcolors.FAIL}[X]{bcolors.ENDC} No API Key Provided")
            return []
        queries = [urllib.parse.quote(query) for query in queries]
        pwww_url = f"https://publicwww.com/websites/\"THE_QUERY\"/?export=urls&key={self.token}"
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
                }
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying PublicWWW...")
        
        domains = {}
        for q in queries:
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
                return [{}, []]
            else:
                domains[uq_q] = [url for url in data.split("\n") if url]
                print(f"  > {uq_q}: {len(domains[uq_q])} results")
        
        return  [domains, [v for x in domains.values() for v in x]]# index 0 is dict using query as keys, 1 is just list of domains
