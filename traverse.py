from traverse import spyonweb, scraper, publicwww, shodanapi, checks, webarchive
from traverse import conf
import api_keys 

import argparse
import json
import os

os.system('') # let colours be used on windows

class RunTraverse:
    def __init__(self, parser, args):
        self.parser = parser
        self.args = args

        self.pwww = publicwww.PublicWWW(api_keys.publicwww)
        self.shodan = shodanapi.ShodanAPI(api_keys.shodankey)

    def fromDomain(self, domain):
        if not checks.validateURL(domain):
            self.parser.error("Please supply a url in a valid format: http(s)://example.tld\n")
        
        spy = spyonweb.SpyOnWeb(api_keys.spyonweb, domain)
        wa = webarchive.WebArchive(domain)
    
        # If you do not want to directly interact with the target domain, do not use the (live) scraper.
        scraped_ids = scraper.scrapeMatch(domain)
        spy_ids = spy.getAnalyticsandAdsense()
        wa_ids = wa.scrapeWebArchive()

        all_analytics = checks.combineLists(scraped_ids["analytics"], spy_ids["analytics"], wa_ids["analytics"])
        all_adsense = checks.combineLists(scraped_ids["adsense"], spy_ids["adsense"], wa_ids["adsense"])
        all_ids = {"analytics": all_analytics, "adsense": all_adsense}
        all_ids_list = checks.combineLists(all_ids["analytics"], all_ids["adsense"])

        spy_domains = spy.getDatafromCodes(all_ids)
        shodan_domains = self.shodan.getDatafromQuery(all_ids_list)

        # PublicWWW seems to implement fairly heavy rate limiting (at least for the free version) so for now it will not be included for domain searches.
        # Uncomment the following line, and remove the current pwww_domains with the commented out version to force publicwww
        # pwww_domains = self.pwww.getDatafromQuery(all_ids_list)
        pwww_domains = [{}, []]
        
        all_domains = checks.combineLists(spy_domains[1], shodan_domains[1], pwww_domains[1])
        json_data = {
        str(domain): {
            "spyonweb": spy_domains[0],
            "shodan": shodan_domains[0],
            }    
        }
        print(f"{chr(10)}{conf.bcolors.CYAN}{chr(10).join(all_domains)}{conf.bcolors.ENDC}")
        return [json_data, all_domains]
    
    def fromString(self, queryString):
        pwww_domains = self.pwww.getDatafromQuery([queryString])
        shodan_domains = self.shodan.getDatafromQuery([queryString])

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
        
        with open(str(filename), 'w') as f:
            f.write('\n'.join(data[1]))
        print(f"\n{conf.bcolors.OKGREEN}[+]{conf.bcolors.ENDC} Wrote to {filename}")
    
    def outputJson(self, data, filename):

        with open(str(filename), 'w') as f:
            json.dump(data[0], f, indent=4)
        print(f"\n{conf.bcolors.OKGREEN}[+]{conf.bcolors.ENDC} Wrote to {filename}")



def main():

    if not api_keys.spyonweb or not api_keys.publicwww or not api_keys.shodankey:
        print(f"""{conf.bcolors.GREY}It is highly recommended to add all api keys.\napi_keys.py:\n
        spyonweb  = "apikey"
        publicwww = "apikey"
        shodankey = "apikey"{conf.bcolors.ENDC}
        """)
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