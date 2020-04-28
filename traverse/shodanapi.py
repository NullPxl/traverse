import shodan
from .conf import bcolors

class ShodanAPI():
    def __init__(self, token: str, queries: list):
        self.token = token
        self.queries = queries
        self.api = shodan.Shodan(token)
    
    def getDatafromQuery(self) -> list:
        info = {}
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying Shodan...")
        try:
            # at the time of testing, using an OR operator just errors out :(
            for q in self.queries:
                search_results = self.api.search(f"html:\"{q}\"")
                if search_results['matches']:
                    for result in search_results['matches']:
                        hosts = [f"{host}:{result['port']}" for host in result['hostnames']]
                        if q in info:
                            info[str(q)].extend(hosts)
                        else:
                            info[str(q)] = hosts
                    print(f"  > {q}: {len(info[q])} results")
                else:
                    print(f"  > {q}: 0 results")
                        
        except shodan.APIError as e:
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} {e}")

        results = []
        for l in info.values():
            results.extend(l)
        return results