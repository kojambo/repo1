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
            #item['title'] =  str.split("kaufen")[0]
            str = item['title'][0]
            if str.count("kaufen") > 0:
                item['title'] =  str[:str.index(" kaufen")]
            if  str.count("bestellen") > 0:
                item['title'] =  str[:str.index(" bestellen")]
            if str.count("versand") > 0:
                item['title'] =  str[:str.index(" versand")]
                
            #item['title'] =  str[:str.index("kaufen")]
            
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

