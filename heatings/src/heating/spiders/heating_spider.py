import scrapy
import time
import random

from heating.items import heatingItem

class heatingSpider(scrapy.Spider):
    name = "heating"
    allowed_domains = ["idealo.de"]
    start_urls = [
        "http://www.idealo.de/preisvergleich/ProductCategory/18406F1529515-1898979.html?param.alternativeView=true&param.resultlist.count=50"
    ]
    # alculate random sleep time
    # obtained from snippet luerichs Scraper Thread   
    def _time_to_wait(self):
        return random.uniform(.5, 1.5)
        
        
    #===========================================================================
    # first version from tutorial
    # def parse(self, response):
    #     for sel in response.xpath('//td'):
    #         title = sel.xpath('a/text()').extract()
    #         link = sel.xpath('a/@href').extract()
    #         desc = sel.xpath('text()').extract()
    #         print title, link, desc
    #===========================================================================

    #===========================================================================
    # second version adjusted to Idealo web page
    # def parse(self, response):
    #     for sel in response.xpath('//tr'):
    #         item = heatingItem()
    #         item['title'] = sel.xpath('td/a[@class="offer-title link-2 webtrekk"]/text()').extract()
    #         item['link'] = sel.xpath('td[@class="va-middle"]/a/@href').extract()
    #         item['pricerange'] = sel.xpath('td[@class="va-middle"]/a/span[@class="price bold nobr block fs-18"]/text()').extract()
    #         
    #         yield item
    #===========================================================================

    #===========================================================================
    # helpful links on working with xpath
    #     http://doc.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths
    #     http://plasmasturm.org/log/xpath101/
    #     http://stackoverflow.com/questions/18433376/xpath-select-certain-child-nodes
    #     
    #     
    #===========================================================================
        
    # third version from main page to subpages
    def parse(self, response):
#        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            for href in response.css("td.info >  a::attr('href')"):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_dir_contents)
   
    
    def parse_dir_contents(self, response):
        for sel in response.xpath('//tr'):
            item = heatingItem()
            #item['title'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()').extract()
            
            # title seems to be in a child node sometimes, read this: http://stackoverflow.com/questions/18433376/xpath-select-certain-child-nodes
            # use selenium and downloader middleware: http://stackoverflow.com/a/31140474/5061417

            ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/script[@type="text/javascript"]/following-sibling::*').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/script[@type="text/javascript"]/node()').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/text()[0]').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/node()').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/text()').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/node()').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/a[2]').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/*').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/script[@type="text/javascript"]/text()').extract()
            ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()[5]').extract()
            ## item['longtitle'] = u' ,'.join(sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/descendant-or-self::*[not(self::script)]/text()').extract())
            ## item['longtitle'] = u' ,'.join(sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()').extract())

            
            
            item['linkwithprice'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/@href').extract()
            time.sleep(self._time_to_wait())
            # sleep time# http://stackoverflow.com/a/28105362/5061417 
            yield item


## bekomme ich alle angezeigten Seiten?
## wie gehe ich die Auswahlkriterien durch?
## 