import shodan
from .conf import bcolors

class ShodanAPI():
    def __init__(self, token: str):
        self.api = shodan.Shodan(token)
    
    def getDatafromQuery(self, queries: list):
        domains = {}
        hosts = []
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Querying Shodan...")
        try:
            # at the time of testing, using an OR operator just errors out :(
            for q in queries:
                esc_q = q.replace('"', '\\"')
                search_results = self.api.search(f"html:\"{esc_q}\"")
                
                if search_results['matches']:
                    
                    for result in search_results['matches']:
                        if result['hostnames']:
                            hosts = [f"{host}:{result['port']}" for host in result['hostnames']]
                        else:
                            ip = f"{result['ip_str']}:{result['port']}" # if you don't want ips, get rid of this and the next line
                            hosts.append(ip)
                        if q in domains:
                            domains[str(q)].extend(hosts)
                        else:
                            domains[str(q)] = hosts
                    print(f"  > {q}: {len(domains[q])} results")
                else:
                    domains[str(q)] = hosts
                    print(f"  > {q}: 0 results")
                        
        except shodan.APIError as e:
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} {e}")
                return [domains, [v for x in domains.values() for v in x]]

        return [domains, [v for x in domains.values() for v in x]] # index 0 is dict using query as keys, 1 is just list of domains