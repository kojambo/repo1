from scrapy.exceptions import DropItem
import urlparse
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class heatingPipeline(object):
    def process_item(self, item, spider):
        if item['linkwithprice']:
            parsed = urlparse.urlparse(item['linkwithprice'][0])
            item['price'] = urlparse.parse_qs(parsed.query)['price']
            item['categoryId'] = urlparse.parse_qs(parsed.query)['categoryId']  
            item['productid'] = urlparse.parse_qs(parsed.query)['productid']    
            item['sid'] = urlparse.parse_qs(parsed.query)['sid']
            if item['desc']:
                item['desc']  = item['desc'][0].replace('\n',' ')
            title_str = item['title'][0]
            if title_str.count("kaufen") > 0:
                item['title'] =  title_str[:title_str.index(" kaufen")]
            if  title_str.count("bestellen") > 0:
                item['title'] =  title_str[:title_str.index(" bestellen")]
            if title_str.count("versand") > 0:
                item['title'] =  title_str[:title_str.index(" versand")]
            if item['header']:
                item['header']  = item['header'].replace('\n',' ')
                
            #item['title'] =  title_str[:title_str.index("kaufen")]
            
            return item
        else:
            raise DropItem("Leer")

       #if item['price']:
       #    return item
       #else:
       #    raise DropItem("Leer")
            
            
        #=======================================================================
        # if not item['linkwithprice']:
        #     if not item['title']:
        #         raise DropItem("Leer")
        #     else:
        #         return item
        # else:
        #     return item
        #=======================================================================

