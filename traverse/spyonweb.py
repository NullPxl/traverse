import requests
from .conf import bcolors



class SpyOnWeb:

    def __init__(self, token: str, domain: str):
        self.token = token
        self.domain = domain

    def getAnalyticsandAdsense(self) -> dict:
        summary_url = f"https://api.spyonweb.com/v1/summary/{self.domain}?access_token={self.token}"
        r = requests.get(summary_url)
        data = r.json()
        ids = {"analytics": [], "adsense": []}
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Checking SpyOnWeb for {self.domain}...")
        if data["status"] == "found":
            print(f"{bcolors.OKGREEN}[&]{bcolors.ENDC} Found {self.domain} on SpyOnWeb...")
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
            print(f"{bcolors.WARNING}[/]{bcolors.ENDC} \"{self.domain}\" was not found on SpyOnWeb.")
            return ids
        elif data["status"] == "error":
            if data["message"] == "unauthorized":
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} Invalid SpyOnWeb API Key provided")
            else:
                raise Exception(f"There was an error: {data['message']}")
            return ids
    

    def getDatafromCodes(self, ids: dict) -> dict:
        # Takes a dict of lists of google analytics and adsense codes and return a list of domains
        domains = {"analytics": [], "adsense": []} # keeping it as a dict to track where domains came from, in case analysis is needed

        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying SpyOnWeb for ids...")
        for id_type in ids:
            for _id in ids[id_type]: # can use id_type to keep track 
                spy_url = f"https://api.spyonweb.com/v1/{id_type}/{_id}?access_token={self.token}"
                r = requests.get(spy_url)
                data = r.json()
                if data["status"] == "found":
                    try:
                        d = data["result"][id_type][_id]["items"]
                        for k in d.keys():
                            domains[id_type].append(k)
                        print(f"  > {_id}: {len(domains[id_type])} results")
                    except KeyError as e:
                        continue
                elif data["status"] == "not_found": # If the domain has not been scraped by spyonweb
                    # print(f"No data found for {_id} in SpyOnWeb")
                    continue
                elif data["status"] == "error":
                    print(f"{bcolors.FAIL}[X]{bcolors.ENDC} There was an error with {_id}: {data['message']}")
                    continue
        return domains # the returned dict is not cleaned up, use check.combineLists to do so.
