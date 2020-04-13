import re
import requests


def validateURL(domain: str) -> bool:
    validators = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    # https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    return (re.match(validators, domain) is not None)

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }

def findGA(domain: str) -> str:
    # UA-[0-9]+-[0-9]+
    try:
        p = re.compile("UA-[0-9]+-[0-9]+", re.IGNORECASE) 
        page = requests.get(domain, headers=headers).text
        results = list(set(p.findall(page)))
        return results
    except:
        raise Exception(f"There was an error making the request to {domain}")
