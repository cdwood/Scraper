
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest


class jsSpiderSpider(scrapy.Spider):
    name = 'jsSpider'
    start_urls = ['https://www.uark.edu/']

    custom_settings = {
        'DEPTH_LIMIT': 2
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait': 0.5},
            )


    def parse(self, response):

        links = []
        linkText = []
        followLinks = []
        print(type(response))

        for link in response.css('a'):
            links.append(link.css("a::attr(href)").get())
            linkText.append(link.css("a::text").get())

        for x in range(len(links)):
            # print("Link Text: " + str(type(linkText[x])))
            if linkText[x] is not None:
                if "Privacy Policy" in linkText[x]:
                    followLinks.append(links[x])
                elif "privacy policy" in linkText[x]:
                    followLinks.append(links[x])
                elif "Terms of Use" in linkText[x]:
                    followLinks.append(links[x])
                elif "Terms & Conditions" in linkText[x]:
                    followLinks.append(links[x])
                elif "Terms & Privacy" in linkText[x]:
                    followLinks.append(links[x])

        for link in followLinks:
            yield {
                'link': link
            }

        for link in followLinks:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parsePolicy)
    

    def parsePolicy (self, response):
        foundText = []
        botText = []

        for text in response.css('*::text').getall():
            foundText.append(text)
        
        for text in foundText:
            if "scraping" in text:
                botText.append(text)
            elif "robot" in text:
                botText.append(text)
            elif "robots" in text:
                botText.append(text)
            elif "scraper" in text:
                botText.append(text)
            elif "scrape" in text:
                botText.append(text)
            elif "crawl" in text:
                botText.append(text)
            elif "crawler" in text:
                botText.append(text)
            elif "crawlers" in text:
                botText.append(text)
        
        for text in botText:
            yield {
                'text': text
            }

        # seen = set()
        # result = []
        # for item in response.css('*::text').re(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"):
        #     if item not in seen:
        #         seen.add(item)
        #         result.append(item)
        # phone = response.css('*::text').re(r"^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$")
        # for x in range(len(result)):
        #     yield {
        #         'phone': phone[x],
        #         'email': result[x]
        #     }
        # linkFollow = []
        # for links in response.css('a::attr(href)').re(r'^(?:\/?\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\(\)\*\+,;=.]+$'):
        #     if "directory" in links:
        #         linkFollow.append(links)
        # for linked in linkFollow:
        #     linked = response.urljoin(linked)
        #     yield scrapy.Request(linked, callback=self.parse)

        # for person in response.css('div.directory_listPeople div.row > div'):
        #     yield {
        #         'title': person.css('div.title::text').getall(),
        #         'name': person.css('div.name::text').getall(),
        #         'phone': person.css('*::text').re(r"^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$"),
        #         'email': person.css('*::text').re(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"),
        #     }
