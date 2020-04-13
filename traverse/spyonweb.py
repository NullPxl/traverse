import requests


class SpyOnWeb:

    def __init__(self, token: str, domain: str):
        self.token = token
        self.domain = domain
    # previsouly getAnalyticsCode
    def getAnalyticsandAdsense(self) -> tuple:
        # When supplied with domain
        summary_url = f"https://api.spyonweb.com/v1/summary/{self.domain}?access_token={self.token}"
        r = requests.get(summary_url)
        data = r.json()
        if data["status"] == "found":
            print(f"Found {self.domain} on SpyOnWeb...")
            try:
                d = (data["result"]["summary"]).values()
                items = list(d)[0]['items']
                if "analytics" in items: analytics_results = list(items['analytics'])
                if "adsense" in items: adsense_results = list(items['adsense'])
                # scraped = findGA(self.domain) # Add together results with scraped, should this be done at the end instead?
                # results.extend(scraped)
                return analytics_results, adsense_results
            except KeyError as e:
                print("There was an error parsing SpyOnWeb data. Skipping.")
                return [], []
        elif data["status"] == "not_found": # If the domain has not been scraped by spyonweb
            print(f"Supplied domain: \"{self.domain}\" was not found.  Skipping.")
            return [], []
        elif data["status"] == "error":
            raise Exception(f"There was an error: {data['message']}")
    
    def getDatafromCodes(self, tracking_ids: tuple) -> list:
        # Takes a tuple of lists of google analytics and adsense codes and return a list of domains
        analytics_codes = tracking_ids[0]
        adsense_codes = tracking_ids[1]

        ga_url = f"https://api.spyonweb.com/v1/analytics/GA_CODE?access_token={self.token}" # analytics
        gad_url = f"https://api.spyonweb.com/v1/adsense/GAD_CODE?access_token={self.token}" # adsense

        info = []
        for code in analytics_codes: # Probably not enough codes in the list to warrant using aiohttp here.
            ga_url = ga_url.replace("GA_CODE", code)
            r = requests.get(ga_url)
            data = r.json()
            if data["status"] == "found":
                if code[-2] == "-":
                    # spyonweb's results don't include the property indicator (# after -)
                    code_key = code[0:-2]
                else:
                    code_key = code
                try:
                    d = data["result"]["analytics"][code_key]["items"]
                    info.append(d)
                except KeyError as e:
                    continue
            elif data["status"] == "not_found": # If the domain has not been scraped by spyonweb
                print(f"No data found for {code} in SpyOnWeb")
                continue
            elif data["status"] == "error":
                print(f"There was an error with {code}... Continuing")
                continue

        for code in adsense_codes:
            gad_url = gad_url.replace("GAD_CODE", code)
            r = requests.get(gad_url)
            data = r.json()
            if data["status"] == "found":
                try:
                    d = data["result"]["adsense"][code]["items"]
                    info.append(d)
                except KeyError as e:
                    continue
            elif data["status"] == "not_found": # If the domain has not been scraped by spyonweb
                print(f"No data found for {code} in SpyOnWeb")
                continue
            elif data["status"] == "error":
                print(f"There was an error with {code}... Continuing")
                continue
        
        
        results = []
        # There is probably a much better way to do this, submit a pull req if you know one!
        for d in info:
            for k in d.keys():
                results.append(k)
        return results


