import re
# import requests


def reformURL(urls: list) -> list:
    scheme_re = re.compile(
        r'^(http)s?://'
    )
    port_re = re.compile(
        r'(:\d+)'
    )
    
    n_urls = []
    for domain in urls:
        port = re.search(port_re, domain)
        scheme = re.search(scheme_re, domain)
        
        if port and not scheme:
            if port.group(0)[1:] == "443":
                domain = "https://" + domain
            else:
                domain = "http://" + domain
        
        elif not scheme and not port:
            domain = "http://" + domain
        
        n_urls.append(domain)
    return n_urls

def validateURL(domain: str):
    # Make sure the url is valid for the requests library
    validators = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    # https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    if domain == None: return False
    return ((re.match(validators, domain) is not None))

def combineLists(*lists) -> list:
    # Combine multiple lists into a single one, and remove any duplicates
    combined_list = []
    for l in lists:
        combined_list.extend(l)
    return list(set(combined_list))
