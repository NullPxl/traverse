import requests
from .conf import bcolors



class SpyOnWeb:

    def __init__(self, token: str):
        self.token = token

    def getAnalyticsandAdsense(self, domain) -> dict:
        # Make a summary call to spyonweb to get all known (to spyonweb) google analytics and adsense ids
        summary_url = f"https://api.spyonweb.com/v1/summary/{domain}?access_token={self.token}"
        r = requests.get(summary_url)
        data = r.json()
        ids = {"analytics": [], "adsense": []}
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Checking SpyOnWeb for {domain}...")
        if data["status"] == "found":
            print(f"  {bcolors.OKGREEN}>{bcolors.ENDC} Found {domain} on SpyOnWeb...")
            try:
                d = (data["result"]["summary"]).values()
                items = list(d)[0]['items']
                if "analytics" in items: 
                    analytics_results = list(items['analytics'])
                    print(f"  > Google Analytics: {len(analytics_results)} results")
                    ids["analytics"].extend(analytics_results)
                else:
                    analytics_results = []
                if "adsense" in items: 
                    adsense_results = list(items['adsense'])
                    print(f"  > Google Adsense: {len(adsense_results)} results")
                    ids["adsense"].extend(adsense_results)
                else:
                    adsense_results = []

                return ids
            
            except KeyError as e:
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} There was an error parsing SpyOnWeb data. Skipping.")
                return ids
        elif data["status"] == "not_found": # If the domain has not been scraped by spyonweb
            print(f"{bcolors.WARNING}[/]{bcolors.ENDC} \"{domain}\" was not found on SpyOnWeb.")
            return ids
        elif data["status"] == "error":
            if data["message"] == "unauthorized":
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} Invalid SpyOnWeb API Key provided")
            else:
                raise Exception(f"There was an error: {data['message']}")
            return ids
    

    def getDatafromCodes(self, ids: dict):
        # Takes a dict of lists of google analytics and adsense codes and return domains
        domains = {} # keeping it as a dict to track where domains came from, in case analysis is needed

        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying SpyOnWeb for ids...")
        for id_type in ids:
            for _id in ids[id_type]: # can use id_type to keep track 
                spy_url = f"https://api.spyonweb.com/v1/{id_type}/{_id}?access_token={self.token}"
                r = requests.get(spy_url)
                data = r.json()
                if data["status"] == "found":
                    try:
                        d = data["result"][id_type][_id]["items"]
                        # print(d)
                        domains[_id] = [k for k in d.keys()]
                        # for k in d.keys():
                        #     domains.setdefault(_id, []).append(k)
                        print(f"  > {_id}: {len(domains[_id])} results")
                    except KeyError as e:
                        continue
                elif data["status"] == "not_found": # If the domain has not been scraped by spyonweb
                    domains[_id] = []
                    print(f"  > {_id}: 0 results")
                    continue
                elif data["status"] == "error":
                    print(f"{bcolors.FAIL}[X]{bcolors.ENDC} There was an error with {_id}: {data['message']}")
                    continue
        return [domains, [v for x in domains.values() for v in x]] # index 0 is dict using ids as keys, 1 is just list of domains
