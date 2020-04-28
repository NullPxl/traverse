from traverse import spyonweb, nerdydata, scraper, publicwww, shodanapi, checks
from traverse import conf
import api_keys 

import argparse
import os

os.system('') # let colours be used

def main():
    
    parser = argparse.ArgumentParser(description="Traverse: Find more hosts from repeated tracking codes and strings.")
    p = parser.add_mutually_exclusive_group()
    # parser.add_argument('-l', '--list', help='file of domains to test', required=True)
    p.add_argument('-d', '--domain', help='The starting domain containing tracking codes. e.x) http://example.com')
    # parser.add_argument('-ga', '--ganalytics', help='Only search for occurences of the supplied google analytics id')
    # parser.add_argument('-gad', '--gadsense', help='Only search for occurences of the supplied google adsense id')
    p.add_argument('-s', '--string', help='A string to search for, skips tracking code specific searches. e.x) "© 2020 Organization Inc."')
    parser.add_argument('-o', '--output', help='file location to output to')
    # TO DO: parser.add_argument('-r', '--recursive', help="WARNING: This will continue to search across all domains found until nothing is returned (meaning a lot of requests)", action='store_true')
    args = parser.parse_args()

    if not checks.validateURL(args.domain) and args.string == None:
        parser.error("Please supply a url in a valid format: http(s)://example.tld\nOR provide a string: --string \"to search for\"")
    if not api_keys.spyonweb or not api_keys.publicwww or not api_keys.shodankey:
        print("""Please add your api keys\napi_keys.py:\n
        spyonweb = "apikey"
        publicwww = "apikey"
        shodankey = "apikey"
        """)
        return
    if args.domain:
        # Uses spyonweb, nerdydata and scrapes the page.
        # If you do not want to directly interact with the target domain, do not use the scraper.
        spy = spyonweb.SpyOnWeb(api_keys.spyonweb, args.domain)

        scraped_ids = scraper.scrapeMatch(args.domain) # returns dict
        spy_ids = spy.getAnalyticsandAdsense() # returns dict

        all_analytics = checks.combineLists(scraped_ids["analytics"], spy_ids["analytics"])
        all_adsense = checks.combineLists(scraped_ids["adsense"], spy_ids["adsense"])
        all_ids = {"analytics": all_analytics, "adsense": all_adsense}
        # print(f"{conf.bcolors.CYAN}All ids: {all_ids}{conf.bcolors.ENDC}")

        all_ids_list = checks.combineLists(all_ids["analytics"], all_ids["adsense"])
        nd = nerdydata.NerdyData(all_ids_list)
        # pwww = publicwww.PublicWWW(api_keys.publicwww, all_ids_list)
        shodan = shodanapi.ShodanAPI(api_keys.shodankey, all_ids_list)

        spy_domains = spy.getDatafromCodes(all_ids) # returns dict
        nd_domains = nd.getDatafromQuery() # returns singular list to keep compatible with just string searches.  May change later.
        # pwww_domains = pwww.getDatafromQuery() # returns singular list like nd_domains
        # PublicWWW seems to implement rate limiting (at least for the free version) so for now it will not be included for domain searches.
        shodan_domains = shodan.getDatafromQuery()

        all_domains = checks.combineLists(spy_domains["analytics"], spy_domains["adsense"], nd_domains, shodan_domains)
        print(f"{chr(10)}{conf.bcolors.CYAN}{chr(10).join(all_domains)}{conf.bcolors.ENDC}")

    
    if args.string:
        # Searches in nerdydata and publicwww currently.
        nd = nerdydata.NerdyData([args.string])
        pwww = publicwww.PublicWWW(api_keys.publicwww, [args.string])
        shodan = shodanapi.ShodanAPI(api_keys.shodankey, [args.string])
        
        nd_domains = nd.getDatafromQuery()
        pwww_domains = pwww.getDatafromQuery()
        shodan_domains = shodan.getDatafromQuery()
        all_domains = checks.combineLists(nd_domains, pwww_domains, shodan_domains)
        print(f"{chr(10)}{conf.bcolors.CYAN}{chr(10).join(all_domains)}{conf.bcolors.ENDC}")

        print("\nNote that free NerdyData results are limited to 10 rows, and free PublicWWW is limited to their top 3M sites")

    if args.output:
        with open(str(args.output), 'w') as f:
            f.write('\n'.join(all_domains))
        print(f"\n{conf.bcolors.OKGREEN}[+]{conf.bcolors.ENDC} Wrote to {args.output}")

if __name__ == "__main__":
    banner = """
    traverse
        ⁻ ᵇʸ ⁿᵘˡˡᵖˣˡ
    """
    print(banner)
    main()