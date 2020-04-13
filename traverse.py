from traverse import spyonweb, nerdydata, checks
import api_keys # Create a file called api_keys.py with the var: spyonweb

domain = "http://example.tld"

if not checks.validateURL(domain):
    raise Exception("Please supply a url in a valid format: http(s)://example.tld")

spyonweb = spyonweb.SpyOnWeb(api_keys.spyonweb, domain)
codes = spyonweb.getAnalyticsCode()
spy_domains = spyonweb.getDatafromCode(codes)

nerdydata = nerdydata.NerdyData(codes)
nd_domains = nerdydata.getDatafromQuery()

spy_domains.extend(nd_domains) # combined
all_domains = list(set(spy_domains))

print(all_domains)
