# Traverse
Expand on known hosts related to a domain through searching for instances of repeated code/html and tracking ids across publically available data.

* Initial idea for this came from reading [this bellingcat blog post](https://www.bellingcat.com/resources/how-tos/2015/07/23/unveiling-hidden-connections-with-google-analytics-ids/)

Traverse currently uses 
* [spyonweb](http://www.spyonweb.com/) [free, requires api key]
* [publicwww](https://publicwww.com) [free, requires api key], 
* [shodan](https://www.shodan.io/) [free up until a certain amount of use, but it's quite a lot of use], 
* [WebArchive](https://web.archive.org/) scraping.
    * This may take a few minutes depending on how many snapshots of the page there are.
* Live page scraping

![domain search example output](https://i.imgur.com/LHb8VYQ.png)
* *`-o` has been changed to `-oS`, meaning output simple (plaintext).  `-oJ` outputs in json*

![search string example output](https://i.imgur.com/FdGjrYZ.png)

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
* Implement [CommonCrawl](http://commoncrawl.org/)
* Recursive search option
* https://www.nerdydata.com Used to be implemented (check commit history), but their api now only allows for 50 free requests before $0.15/query, so I took it out (as of now)