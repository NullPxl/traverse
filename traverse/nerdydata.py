import requests
import urllib.parse

class NerdyData:
    # Used when a string or list of strings is provided to search for across sites.
    # Not necessarily just tracking ids, can also be copyright strings or reused code.

    def __init__(self, queries: list):
        # queries[0].extend(queries[1]) # combining the lists in the tuple of queries
        # combined = list(set(queries[0]))
        self.queries = [urllib.parse.quote(query) for query in queries]

    
    def getDatafromQuery(self) -> list:
        # Returns a list of domains associated with the queries
        nd_url = "https://api.nerdydata.com/search?query=THE_QUERY"
        headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
                }
        info = []
        print("Querying NerdyData...")
        for q in self.queries:
            r = requests.get(nd_url.replace("THE_QUERY", q), headers=headers)
            data = r.json()
            # print(data)
            info.append(data)
        print("Got results from NerdyData.")
        results = [] # domains
        for result in info:
            if result['total'] > 0:
                for site in range(len(result['sites'])):
                    print(f"Found {result['sites'][site]['domain']}")
                    results.append(result['sites'][site]['domain'])
        return results