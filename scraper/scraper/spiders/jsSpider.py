
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
        print(type(response))

        for link in response.css('a'):
            # newLink = link.css('a::attr(href').get()
            # links.append(newLink)
            # text = link.css(a::text).get()
            # newLinkText = link.css('a::text').get()
            # linkText.append(newLinkText)
            yield {
                'link': link.css("a::attr(href)").get(),
                'text': link.css("a::text").get()
            }
        
        print("Link array length: " + len(links))
        print("Link Text Array Length: " + len(linkText))

        # privacy = [k for k in links if '']
        # print(links)


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
