import re
# import requests


def validateURL(domain: str) -> bool:
    # Make sure the url is valid for the requests library
    validators = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    # https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    if domain == None: return False
    return (re.match(validators, domain) is not None)

def combineLists(*lists) -> list:
    # Combine multiple lists into a single one, and remove any duplicates
    combined_list = []
    for l in lists:
        combined_list.extend(l)
    return list(set(combined_list))
