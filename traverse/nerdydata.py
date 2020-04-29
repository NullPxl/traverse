import requests
import urllib.parse
from .conf import bcolors

class NerdyData:
    # Used when a string or list of strings is provided to search for across sites.
    # Not necessarily just tracking ids, can also be copyright strings or reused code.

    def __init__(self):
        pass

    
    def getDatafromQuery(self, queries: list) -> list:
        # Returns a list of domains associated with the queries
        nd_queries = []
        for q in queries:
            if len(q) > 45:
                print(f"{bcolors.WARNING}[/]{bcolors.ENDC} NerdyData only accepts strings less than or equal to 45 characters, shortening the string.")
                q = q[:45]
            nd_queries.append(urllib.parse.quote(q))

        nd_url = "https://api.nerdydata.com/search?query=THE_QUERY"
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
                }
        info = {}
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying NerdyData...")
        for q in nd_queries:
            r = requests.get(nd_url.replace("THE_QUERY", q), headers=headers)
            data = r.json()
            uq_q = urllib.parse.unquote(str(q))
            # print(f"\t{uq_q}: {data['total']} results") returns all potential data, not necessarily available to user.

            info[uq_q] = data

        results = []
        for query, response in info.items():
            try:
                print(f"  > {query}: {len(response['sites'])} results")
                for site in response['sites']:
                    results.append(site['url'])
            except:
                print(f"{bcolors.WARNING}[/]{bcolors.ENDC} {response['message']}")
        return results
