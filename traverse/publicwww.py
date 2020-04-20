import api_keys
import urllib.parse
import requests

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
        print("Querying PublicWWW...\n")
        
        # info = {}
        info = []
        for q in self.queries:
            r = requests.get(pwww_url.replace("THE_QUERY", q), headers=headers)
            data = r.text
            if data == "Wrong API key":
                print("Invalid PublicWWW API Key provided.")
                return []
            else:
                # info[urllib.parse.unquote(str(q))] = [url for url in data.split("\n") if url]
                for url in data.split("\n"):
                    if url:
                        # print(f"publicwww found: {url}")
                        info.append(url)
        return info
