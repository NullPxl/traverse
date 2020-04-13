import requests
from .checks import findGA


class SpyOnWeb:

    def __init__(self, token: str, domain: str):
        self.token = token
        self.domain = domain
    
    def getAnalyticsCode(self) -> list:
        # When supplied with domain
        summary_url = f"https://api.spyonweb.com/v1/summary/{self.domain}?access_token={self.token}"
        r = requests.get(summary_url)
        data = r.json()
        if data["status"] == "found":
            print(f"Found {self.domain} on SpyOnWeb...")
            try:
                d = (data["result"]["summary"]).values()
                items = list(d)[0]['items']
                results = list(items['analytics'])
                scraped = findGA(self.domain) # Add together results with scraped, should this be done at the end instead?
                results.extend(scraped)
                return list(set(results))
            except KeyError as e:
                print("No analytics codes found, scraping the page.")
                ga_ids = findGA(self.domain)
                return ga_ids

        elif data["status"] == "not_found": # If the domain has not been scraped by spyonweb
            print(f"Supplied domain: \"{self.domain}\" was not found, looking for analytics code inside of page source...")
            ga_ids = findGA(self.domain)
            return ga_ids
        elif data["status"] == "error":
            raise Exception(f"There was an error: {data['message']}")
    
    def getDatafromCode(self, analytics_codes: list) -> list:
        # Takes a list of GA codes and returns domains
        ga_url = f"https://api.spyonweb.com/v1/analytics/GA_CODE?access_token={self.token}"

        info = []
        for code in analytics_codes: # Probably not enough codes in the list to warrant using aiohttp here.
            url = ga_url.replace("GA_CODE", code)
            r = requests.get(url)
            data = r.json()
            if data["status"] == "found":
                # print(data)
                if code[-2] == "-":
                    # spyonweb's results don't include the -# indicator
                    code_key = code[0:-2]
                else:
                    code_key = code
                d = data["result"]["analytics"][code_key]["items"]
                info.append(d)

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


