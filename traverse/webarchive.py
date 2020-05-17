import requests
import asyncio
from aiohttp import ClientSession, ClientTimeout
from aiohttp import client_exceptions
import os
import sys
import random
import re

from .scraper import matcher
from .checks import combineLists
from .conf import bcolors

class WebArchive:
    def __init__(self, domain):
        self.domain = domain
        self.ids = {"analytics": [], "adsense": []}
    
    def getAllArchives(self):
        # gets a list of timestamps for all unique pages saved from web archive
        r = requests.get(f"https://web.archive.org/cdx/search/cdx?url={self.domain}&fl=timestamp,digest&output=json&showResumeKey=true")
        j = [i for i in r.json() if i]
        seen_digests = []
        res = []
        for time in [time for time in j if len(time[0]) == 14]: # Initial
            if time[1] not in seen_digests:
                res.append(time[0])
                seen_digests.append(time[1])
        
        try:
            while "+" in j[-1][0]: # If there is a resume key (hit limit)
                resumekey = j[-1][0]
                r = requests.get(f"https://web.archive.org/cdx/search/cdx?url={self.domain}&fl=timestamp,digest&output=json&showResumeKey=true&resumeKey={resumekey}")
                j = [i for i in r.json() if i]
                for time in [time for time in j if len(time[0]) == 14]:
                    if time[1] not in seen_digests:
                        res.append(time[0])
                        seen_digests.append(time[1])
            print(f"  > Found {len(res)} unique archives")
        except IndexError:
            print(f"{bcolors.WARNING}[/]{bcolors.ENDC} No archives were found.")
        
        return res

    # use aiohttp for this
    async def parse(self, session, sem, url):
        user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
        
        async with sem:
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent}
            html = ""
            try:
                async with session.get(url, headers=headers) as response:
                    r = await response.read()
                    html = str(r)
            except client_exceptions.ClientResponseError as e:
                # https://github.com/aio-libs/aiohttp/pull/4696
                r = requests.get(url, headers=headers)
                html = str(r.content)
            except asyncio.TimeoutError:
                print(f"{bcolors.WARNING}[/]{bcolors.ENDC} Timeout on {url}, continuing.")
            except Exception as e:
                print(f"{bcolors.FAIL}[X]{bcolors.ENDC} Error occured on {url}: {e}, skipping.")
            scraped = matcher(html, self.ids)
            if scraped:
                self.ids = {"analytics": combineLists(self.ids["analytics"], scraped["analytics"]), "adsense": combineLists(self.ids["adsense"], scraped["adsense"])}
    
    async def getIDs(self):
        tasks = []
        sem = asyncio.Semaphore(5) # don't be mean :)
        timeout = ClientTimeout(total=30)
        async with ClientSession(timeout=timeout) as session:
            timestamps = self.getAllArchives()
            # print(timestamps)
            urls = [f"https://web.archive.org/web/{ts}/{self.domain}" for ts in timestamps]
            for url in urls:
                task = asyncio.ensure_future(self.parse(session, sem, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
        return self.ids

    def scrapeWebArchive(self):
        print(f"{bcolors.OKGREEN}[+]{bcolors.ENDC} Scraping Archives (web.archive.org) of {self.domain}...")
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.getIDs())
        ids = loop.run_until_complete(future)
        return ids
