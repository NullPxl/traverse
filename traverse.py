from traverse import spyonweb, nerdydata, scraper, checks
import api_keys # Create a file called api_keys.py with the var: spyonweb

domain = "http://fullmooncalendar.net"

if not checks.validateURL(domain):
    raise Exception("Please supply a url in a valid format: http(s)://example.tld")

spyonweb = spyonweb.SpyOnWeb(api_keys.spyonweb, domain)

scraped_ids = scraper.scrapeMatch(domain) # returns dict
spy_ids = spyonweb.getAnalyticsandAdsense() # returns dict

all_analytics = checks.combineLists(scraped_ids["analytics"], spy_ids["analytics"])
all_adsense = checks.combineLists(scraped_ids["adsense"], spy_ids["adsense"])
all_ids = {"analytics": all_analytics, "adsense": all_adsense}
print(f"All ids: {all_ids}")

all_ids_list = checks.combineLists(all_ids["analytics"], all_ids["adsense"])
nd = nerdydata.NerdyData(all_ids_list)

spy_domains = spyonweb.getDatafromCodes(all_ids) # returns dict
# print(f"spy domains: {spy_domains}")
nd_domains = nd.getDatafromQuery() # returns singular list, will change later
# print(f"nd domains: {nd_domains}")

all_domains = checks.combineLists(spy_domains["analytics"], spy_domains["adsense"], nd_domains)
print(f"{chr(10)}all domains: {all_domains}")
