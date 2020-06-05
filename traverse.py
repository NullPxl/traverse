from traverse import spyonweb, scraper, publicwww, shodanapi, checks, webarchive
from traverse import conf

import argparse
import json
import os

os.system('') # let colours be used on windows


spyonweb_key = ""
publicwww_key = ""
shodan_key = ""

if not spyonweb_key or not publicwww_key or not shodan_key:
    print(f"""{conf.bcolors.GREY}It is recommended to add all api keys (at the top of the file) for best results\n
    https://api.spyonweb.com/
    https://publicwww.com/prices.html
    https://developer.shodan.io/api/requirements{conf.bcolors.ENDC}""")

api_keys = {"spyonweb": spyonweb_key, "publicwww": publicwww_key, "shodan": shodan_key}
# You may not always want to use every service, or you may not have an api key.
services = ["spyonweb", "publicwww", "shodan", "live_scrape", "webarchive"]
# If you do not want to directly interact with the site, remove live_scrape from the services list above.

default_dict = {"analytics": [], "adsense": []}
default_domains = [{}, []]

class RunTraverse:
    def __init__(self, parser, args):
        self.parser = parser
        self.args = args
        

        self.pwww = publicwww.PublicWWW(publicwww_key)
        self.shodan = shodanapi.ShodanAPI(shodan_key)
        self.spy = spyonweb.SpyOnWeb(spyonweb_key)

    def fromDomain(self, domain):
        domain = checks.reformURL([domain])[0]
        if not checks.validateURL(domain):
            self.parser.error("Please supply a url in a valid format: http(s)://example.tld\n")
        
        # If you do not want to directly interact with the target domain, do not use the (live) scraper.
        scraped_ids = default_dict
        if "live_scrape" in services:
            scraped_ids = scraper.scrapeMatch(domain)

        wa_ids = default_dict
        if "webarchive" in services:
            wa = webarchive.WebArchive(domain)
            wa_ids = wa.scrapeWebArchive()
        
        spy_ids = default_dict
        if "spyonweb" in services and api_keys["spyonweb"]:
            spy_ids = self.spy.getAnalyticsandAdsense(domain)

        # Cleaning up and combining the data found by the modules
        all_analytics = checks.combineLists(scraped_ids["analytics"], spy_ids["analytics"], wa_ids["analytics"])
        all_adsense = checks.combineLists(scraped_ids["adsense"], spy_ids["adsense"], wa_ids["adsense"])
        all_ids = {"analytics": all_analytics, "adsense": all_adsense}
        all_ids_list = checks.combineLists(all_ids["analytics"], all_ids["adsense"])
        
        # Query services with the discovered ids to return associated domains
        spy_domains = default_domains
        if "spyonweb" in services and api_keys["spyonweb"]:
            spy_domains = self.spy.getDatafromCodes(all_ids)
        
        shodan_domains = default_domains
        if "shodan" in services and api_keys["shodan"]:
            shodan_domains = self.shodan.getDatafromQuery(all_ids_list)

        pwww_domains = default_domains
        # PublicWWW seems to implement fairly heavy rate limiting (at least for the free version) so for now it will not be included for domain searches.
        # Uncomment the following 2 lines to force publicwww
        # if "publicwww" in services:
        #   pwww_domains = self.pwww.getDatafromQuery(all_ids_list)
        
        # Generate output types
        all_domains = checks.combineLists(spy_domains[1], shodan_domains[1], pwww_domains[1])
        json_data = {
        str(domain): {
            "spyonweb": spy_domains[0],
            "shodan": shodan_domains[0],
            "publicwww": pwww_domains[0]
            }    
        }
        print(f"{chr(10)}{conf.bcolors.CYAN}{chr(10).join(all_domains)}{conf.bcolors.ENDC}")
        return [json_data, all_domains]
    
    def fromString(self, queryString):
        
        pwww_domains = default_domains
        if "publicwww" in services and api_keys["publicwww"]:
            pwww_domains = self.pwww.getDatafromQuery([queryString])
        
        shodan_domains = default_domains
        if "shodan" in services and api_keys["shodan"]:
            shodan_domains = self.shodan.getDatafromQuery([queryString])
        # Queries are passed via list so it's much easier to implement searching strings via a list in a file

        all_domains = checks.combineLists(pwww_domains[1], shodan_domains[1])
        json_data = {
        str(queryString): {
            "publicwww": pwww_domains[0],
            "shodan": shodan_domains[0],
            }    
        }
        print(f"{chr(10)}{conf.bcolors.CYAN}{chr(10).join(all_domains)}{conf.bcolors.ENDC}")
        print(f"{chr(10)}{conf.bcolors.WARNING}Note that free PublicWWW is limited to their top 3M sites{conf.bcolors.ENDC}")
        return [json_data, all_domains]
    
    def outputSimple(self, data, filename):
        # Extremely simple output (as the name would imply), just puts all the domains in a text file
        with open(str(filename), 'w') as f:
            f.write('\n'.join(data[1]))
        print(f"\n{conf.bcolors.OKGREEN}[+]{conf.bcolors.ENDC} Wrote to {filename}")
    
    def outputJson(self, data, filename):
        # Good for some analysis, will make it easier to attribute ids/strings to domains
        with open(str(filename), 'w') as f:
            json.dump(data[0], f, indent=4)
        print(f"\n{conf.bcolors.OKGREEN}[+]{conf.bcolors.ENDC} Wrote to {filename}")



def main():

    parser = argparse.ArgumentParser(description="Traverse: Find more hosts from repeated tracking codes and strings.")
    p = parser.add_mutually_exclusive_group()
    # parser.add_argument('-l', '--list', help='file of domains to test')
    p.add_argument('-d', '--domain', help='The starting domain containing tracking codes. e.x) http://example.com')
    # parser.add_argument('-ga', '--ganalytics', help='Only search for occurences of the supplied google analytics id')
    # parser.add_argument('-gad', '--gadsense', help='Only search for occurences of the supplied google adsense id')
    p.add_argument('-s', '--string', help='A string to search for, skips tracking code specific searches. e.x) "© 2020 Organization Inc."')
    output = parser.add_mutually_exclusive_group()
    output.add_argument('-oS', '--outputsimple', help='file location to output plaintext domains to')
    output.add_argument('-oJ', '--outputjson', help='file location to output json structured domains to')
    args = parser.parse_args()
    
    t = RunTraverse(parser, args)
    if args.domain:
        data = t.fromDomain(args.domain)
    if args.string:
        data = t.fromString(args.string)
    
    if args.outputsimple:
        t.outputSimple(data, args.outputsimple)
    if args.outputjson:
        t.outputJson(data, args.outputjson)




if __name__ == "__main__":
    banner = """
    traverse
        ⁻ by nullpxl
    """
    print(banner)
    main()