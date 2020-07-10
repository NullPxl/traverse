# Traverse
Expand on known hosts related to a domain through searching for instances of repeated code/html and tracking ids across publically available data.

* Initial idea for this came from reading [this bellingcat article](https://www.bellingcat.com/resources/how-tos/2015/07/23/unveiling-hidden-connections-with-google-analytics-ids/)

Traverse currently uses 
* [host.io](https://host.io/) [free, requires api key]
* [spyonweb](http://www.spyonweb.com/) [free, requires api key]
* [publicwww](https://publicwww.com) [free, requires api key], 
* [shodan](https://www.shodan.io/) [free, requires api key (premium api keys are regularly available for free or a low price)], 
* [WebArchive](https://web.archive.org/) scraping.
    * This may take some time depending on how many snapshots of the page there are.
    * Disabled by default, to enable it open traverse.py and add "webarchive" to the 'services' list.
* Live page scraping

I wrote a [blog post going into detail on this topic](https://nullpxl.com/post/finding-relationships-between-sites-from-a-page-source/), some ideas referenced in the post have not yet been implemented. 

There are 2 output formats: `-oS` (output simple) which is just a plain text output of discovered domains, and `-oJ` (output json) which is a more detailed JSON output.

![domain search example output](https://i.imgur.com/kWD8FWt.png)

![search string example output](https://i.imgur.com/FdGjrYZ.png)

## Alternative resources that I (most likely) won't add support for in this tool:

* https://httparchive.org/ / BigQuery is amazing for things like this, but also very expensive :( If you have the resources, definitely look into using this great dataset.

* https://xaviesteve.com/domeye/ is also great, but I'll avoid scripting it as it seems to be run and paid for by an individual.

* https://dnslytics.com/reverse-analytics is good but requires payment for most features that separate it from others (no free api)

TODO:
* Facebook Pixel
* Google Tag Manager
* Quantcast
* Yandex Metrika
* Recursive Search
* CommonCrawl (?)