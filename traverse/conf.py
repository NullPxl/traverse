class bcolors:
    HEADER = '\033[95m'
    GREY = '\033[90m'
    OKBLUE = '\033[94m'
    CYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

api_keys_structure = f"""{bcolors.GREY}Create this file\napi_keys.py:\n
        spyonweb  = "apikey" # https://api.spyonweb.com/
        publicwww = "apikey" # https://publicwww.com/prices.html
        shodankey = "apikey" # https://developer.shodan.io/api/requirements{bcolors.ENDC}"""