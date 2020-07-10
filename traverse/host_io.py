import requests
import tldextract
from .conf import bcolors

class HostIO:

    def __init__(self, token: str):
        self.token = token

    def getIDs(self, domain) -> dict:
        # host.io does not support subdomains, and only logs 1 google adsense/analytics.  They will soon be adding support for GTM
        searchable_domain = tldextract.extract(domain).registered_domain # extract just the domain so it can be searchable on host.io
        summary_url = f"https://host.io/api/web/{searchable_domain}?token={self.token}"
        r = requests.get(summary_url)
        ids = {"analytics": [], "adsense": []}
        # if domain != searchable_domain:
        #     print(f"Using '{searchable_domain}' instead of '{domain}' to allow for searching on host.io")
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Checking Host.io for {searchable_domain}...")
        if r.status_code != 200:
            if "No details found" in r.text:
                print(f"{bcolors.WARNING}[/]{bcolors.ENDC} {searchable_domain} was not found on Host.io")
            else:
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} Error retrieving data for {searchable_domain}")
            return ids

        data = r.json()
        if "googleanalytics" in data:
            print(f"  > [Google Analytics]: {data['googleanalytics']}")
            ids["analytics"].append(data["googleanalytics"])
        if "adsense" in data:
            print(f"  > [Google Adsense]: {data['adsense']}")
            ids["adsense"].append(data["adsense"])
        return ids
    
    def getDatafromCodes(self, ids: dict):
        # Takes a dict of lists of google analytics and adsense codes and return domains
        domains = {}
        ids["googleanalytics"] = ids.pop("analytics") 
        # I do this so the key name can act as both a key and host.io endpoint
        
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying Host.io for ids...")
        for id_type in ids:
            for _id in ids[id_type]:
                r = requests.get(f"https://host.io/api/domains/{id_type}/{_id}?limit=1000&token={self.token}")
                if r.status_code != 200:
                    if "No details on" in r.text:
                        print(f"  > {_id}: 0 results")
                    else:
                        print(f"{bcolors.FAIL}[X]{bcolors.ENDC} Error retrieving data for {_id}")
                    domains[_id] = []
                    continue
                data = r.json()
                # if not data:
                #     domains[_id] = []
                #     continue
                domains[_id] = data["domains"]
                print(f"  > {_id}: {len(domains[_id])} results")
        return [domains, [v for x in domains.values() for v in x]]