# Traverse
Instead of focusing on DNS or CT logs, the goal of this tool is to expand on known hosts related to the original domain through searching for instances of repeated code/html and tracking ids across publically available apis/datasets.

* Initial idea for this came from reading [this bellingcat blog post](https://www.bellingcat.com/resources/how-tos/2015/07/23/unveiling-hidden-connections-with-google-analytics-ids/)

Traverse currently uses [spyonweb](http://www.spyonweb.com/) [free, requires api key], [nerdydata](https://www.nerdydata.com/), [publicwww](https://publicwww.com) [free, requires api key], [shodan](https://www.shodan.io/) [free up until a certain amount of use], and page scraping to look for and retrieve data from google analytics and adsense ids, or a user supplied string.

> this output is slightly outdated
![search string example output](https://i.imgur.com/V9FIp8D.png)
![domain search example output](https://i.imgur.com/3IOu3Qt.png)

## Alternative resources that I (most likely) won't add support for in this tool:

* https://httparchive.org/ / BigQuery is amazing for things like this, but also very expensive :(

* https://xaviesteve.com/domeye/ is also great, but I'll avoid scripting it as it seems to be run and paid for by an individual.

* https://dnslytics.com/reverse-analytics is good but requires payment for most features that separate it from others (no free api)

## More ideas: 
* Support Facebook Pixel
* Suggested Google dorks and Query strings (for nerdydata, publicwww, etc.)
    * copyright strings
    * custom js libraries
    * author comments
    * etc
* Scrape WebArchive pages
* Implement [CommonCrawl](http://commoncrawl.org/)
* Recursive search option