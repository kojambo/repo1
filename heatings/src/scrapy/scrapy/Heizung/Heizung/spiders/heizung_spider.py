import scrapy

from Heizung.items import HeizungItem

class HeizungSpider(scrapy.Spider):
    name = "Heizung"
    allowed_domains = ["idealo.de"]
    start_urls = [
        "http://www.idealo.de/preisvergleich/ProductCategory/18406F1529515-1898977-1898979-5346052-5392980.html?param.alternativeView=true&param.resultlist.count=50",
        "http://www.idealo.de/preisvergleich/ProductCategory/18406F1529515-1898977-1898979-5346052-5392980I16-15.html?param.alternativeView=true&param.resultlist.count=50",
        "http://www.idealo.de/preisvergleich/ProductCategory/18406F1529515-1898977-1898979-5346052-5392980I16-30.html?param.alternativeView=true&param.resultlist.count=50"
    ]

    #def parse(self, response):
    #    for sel in response.xpath('//td'):
    #        title = sel.xpath('a/text()').extract()
     #       link = sel.xpath('a/@href').extract()
       #     desc = sel.xpath('text()').extract()
      #      print title, link, desc

    def parse(self, response):
        for sel in response.xpath('//tr'):
            item = HeizungItem()
            #item['title'] = sel.xpath('td/a[@class="offer-title link-2 webtrekk"]/text()').extract()
            item['link'] = sel.xpath('td[@class="va-middle"]/a/@href').extract()
            yield item
