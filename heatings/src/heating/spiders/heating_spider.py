import scrapy
import time
import random

from heating.items import heatingItem
#from selenium import webdriver

class heatingSpider(scrapy.Spider):
    name = "heating"
    allowed_domains = ["idealo.de"]
    start_urls = [
                  "http://www.idealo.de/preisvergleich/ProductCategory/18459F1574288.html?param.alternativeView=true&param.resultlist.count=50"
    ]

    #===========================================================================
    # start_urls = [
    #               "file:///D:/Doku/workspace/heatings/src/heating/html_pages/GasBW12_13kW.htm"
    # ]
    #===========================================================================
        
# http://www.idealo.de/preisvergleich/ProductCategory/18406F1759451.html #oel
# http://www.idealo.de/preisvergleich/ProductCategory/18406F1529515.html #gas
# http://www.idealo.de/preisvergleich/ProductCategory/18406F1529521.html # holz
# http://www.idealo.de/preisvergleich/ProductCategory/18406F1532115.html # pellets
# http://www.idealo.de/preisvergleich/ProductCategory/18459F1574288.html # LW WP
# http://www.idealo.de/preisvergleich/ProductCategory/18459F1783655.html # SW WP
# http://www.idealo.de/preisvergleich/ProductCategory/18459F1574289.html # WW WP




    # calculate random sleep time
    # obtained from snippet luerichs Scraper Thread   
    def _time_to_wait(self):
        return random.uniform(.1, .3)
    
        
    # third version from main page to subpages
    def parse(self, response):
        for number,row in enumerate(response.css("td.va-middle >  a::attr('href')")):    
            url     = response.urljoin(row.extract())
            kw      = response.xpath('//td[@class="info"]/p[@class="lh-16"]/text()').re(r'rmeleistung: (.*) kW')[number]
            info      = response.xpath('//td[@class="info"]/p[@class="lh-16"]/text()').extract()[number]
            header  = response.xpath('//td[@class="info"]/a[@class="offer-title link-2 webtrekk"]/text()').extract()[number]      
               
            request = scrapy.Request(url, callback=self.parse_dir_contents, meta={'kw': kw, 'header': header, 'info':info})
            yield request
                  
        next_page = response.css("div.inner > a.page-next::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
   
    
    def parse_dir_contents(self, response):
        print response
        #item = heatingItem() 
        #my_driver = webdriver.PhantomJS()
        #my_driver.get(response.url)
        #results = my_driver.find_elements_by_xpath('//table[contains(@class, "modular")]//tr[.//a]')
        #for row in results:
        #    item['desc'] = row.find_element_by_xpath('./td[@class="title"]/a').text
        item = heatingItem()
        item['kw'] = response.meta['kw']
        item['header'] = response.meta['header']
        item['info'] = response.meta['info']        
        for sel in response.xpath('//tr'):
            #item = heatingItem()
            #item['kw'] = sel.meta['kw']
            item['title'] = sel.xpath('td[@class="cta"]/a/img[@class="btn-cta-shop"]/@alt').extract()
            item['desc'] = sel.xpath('td/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()').extract()
            item['linkwithprice'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/@href').extract()
            time.sleep(self._time_to_wait())
            # sleep time# http://stackoverflow.com/a/28105362/5061417 
            yield item
            
        next_page_sub = response.css("div.pagination > div.inner > a.page-next::attr('href')")
        if next_page_sub:
            url = response.urljoin(next_page_sub[0].extract())
            yield scrapy.Request(url, self.parse_dir_contents)


## wie gehe ich die Auswahlkriterien durch?



            #item['title'] = sel.xpath('h1[@class="heading-1"]/text()').extract()
            #===================================================================
            # # title seems to be in a child node sometimes, read this: http://stackoverflow.com/questions/18433376/xpath-select-certain-child-nodes
            # # use selenium and downloader middleware: http://stackoverflow.com/a/31140474/5061417
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/script[@type="text/javascript"]/following-sibling::*').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/script[@type="text/javascript"]/node()').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/text()[0]').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/node()').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/text()').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/node()').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/a[2]').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/*').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/script[@type="text/javascript"]/text()').extract()
            # ## item['longtitle'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()[5]').extract()
            # ## item['longtitle'] = u' ,'.join(sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/descendant-or-self::*[not(self::script)]/text()').extract())
            # ## item['longtitle'] = u' ,'.join(sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()').extract())
            #===================================================================

        #=======================================================================
        # for sel in response.xpath('//tr'):
        #     item = heatingItem()
        #     item['title'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()').extract()
        #     item['linkwithprice'] = sel.xpath('td[@class="title"]/a[@class="offer-title link-2 webtrekk wt-prompt"]/@href').extract()
        #=======================================================================


        #item['price'] = sel.xpath('a/span[@class="price"]/text()').extract() #uses div in response.xpath

        #        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):

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
