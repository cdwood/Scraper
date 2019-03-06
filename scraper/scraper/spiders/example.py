
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'directory'
    start_urls = ['https://computer-science-and-computer-engineering.uark.edu/directory/index.php']

    def parse(self, response):
        seen = set()
        result = []
        for item in response.css('*::text').re(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"):
            if item not in seen:
                seen.add(item)
                result.append(item)
        phone = response.css('*::text').re(r"^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$")
        for x in range(len(result)):
            yield {
                'phone': phone[x],
                'email': result[x]
            }
        linkFollow = []
        for links in response.css('a::attr(href)').re(r'^(?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\(\)\*\+,;=.]+$'):
            if "directory" in links:
                linkFollow.append(links)
            # yield {
            #     'links': links#.css('*').re(r'^(?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\(\)\*\+,;=.]+$')
            # }
        for linked in linkFollow:
            linked = response.urljoin(linked)
            yield scrapy.Request(linked, callback=self.parse)

        # for person in response.css('div.directory_listPeople div.row > div'):
        #     yield {
        #         'title': person.css('div.title::text').getall(),
        #         'name': person.css('div.name::text').getall(),
        #         'phone': person.css('*::text').re(r"^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$"),
        #         'email': person.css('*::text').re(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}"),
        #     }
