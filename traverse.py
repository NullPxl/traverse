from traverse import spyonweb, nerdydata, scraper, checks
import api_keys # Create a file called api_keys.py with the var: spyonweb

domain = "http://example.tld"

if not checks.validateURL(domain):
    raise Exception("Please supply a url in a valid format: http(s)://example.tld")

scraped_ids = scraper.scrapeMatch(domain)

spyonweb = spyonweb.SpyOnWeb(api_keys.spyonweb, domain)
spy_ids = spyonweb.getAnalyticsandAdsense()

scraped_ids[0].extend(spy_ids[0])
scraped_ids[1].extend(spy_ids[1])
all_ids = scraped_ids
print(f"All ids: {all_ids}")

nd = nerdydata.NerdyData(all_ids)
spy_domains = spyonweb.getDatafromCodes(all_ids)
nd_domains = nd.getDatafromQuery()
spy_domains.extend(nd_domains)
all_domains = list(set(spy_domains))

print(f"{chr(10).join(all_domains)}")
