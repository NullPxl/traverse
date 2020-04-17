import re
# import requests


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

def combineLists(*lists):
    combined_list = []
    for l in lists:
        combined_list.extend(l)
    return list(set(combined_list))
