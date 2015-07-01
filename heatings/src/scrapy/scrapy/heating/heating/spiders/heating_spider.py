import scrapy

from heating.items import heatingItem

class heatingSpider(scrapy.Spider):
    name = "heating"
    allowed_domains = ["idealo.de"]
    start_urls = [
        "http://www.idealo.de/preisvergleich/OffersOfProduct/3860234_-triocondens-bgb-15-e-erdgas-l-ll-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3588263_-ecoheat-prokondens-hs-15-intercal.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3236450_-cerapur-comfort-eco-zsbe-16-3-a-31-fluessiggas-p-16-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3230045_-triocondens-bgb-15-e-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3139593_-cerapurmodul-solar-zbs-14-210-s-3-ma-31-fluessiggas-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3132736_-cerapursolar-comfort-csw-14-75-3-a-21-erdgas-l-ll-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3132730_-cerapursolar-comfort-csw-14-75-3-a-23-erdgas-e-h-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3116572_-cerapureco-zsb-14-3-e-23-erdgas-e-h-14-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3086181_-thision-s-duo-13-1-elco-heating.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2920543_-logamax-plus-gb172-14-t150-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2654431_-thermo-unit-wtu-15-s-b-weishaupt.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2354011_-smartron-2-13c-elco-heating.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1064608_-ecotherm-plus-wgb-15-e-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2654395_-thermo-condens-wtc-15-a-14-7-kw-weishaupt.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2467626_-logamax-plus-gb172-14-15-1-kw-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3664000_-vitodens-200-w-13-kw-viessmann.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2920589_-logamax-plus-gb172-14-t-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4221070_-logaplus-paket-w9-gb162-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1223708_-vitodens-300-w-11-kw-viessmann.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4661902_-bluestream-cgb-2-14-14-kw-wolf-heizsysteme.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1219746_-cerapur-comfort-eco-zsbe-16-3-a-16-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2286153_-calenta-15-ds-15-8-kw-de-dietrich-remeha.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4278877_-logaplus-paket-k61-gb-212-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4206548_-logaplus-paket-w9-gb162-15-s160rw-rc300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4203081_-logaplus-paket-w30-gb172-14-t150s-erdgas-l-ll-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4199770_-logaplus-paket-w30-gb172-14-t150s-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3738818_-calora-tower-gas-15s-de-dietrich-remeha.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1262303_-vitodens-333-f-11-kw-viessmann.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2286143_-ecotec-exclusiv-vc-146-4-7-vaillant.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2920573_-logamax-plus-gb172-14-t210sr-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3169125_-ecotherm-wbs-14-f-14kw-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184700_-logaplus-paket-w24-s-gb172-14-rc-300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184694_-logaplus-paket-w22-gb172-14-erdgas-e-h-rc-300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184691_-logaplus-paket-w22-s-gb172-14-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184690_-logaplus-paket-w22s-gb172-14-erdgas-e-h-rc-300-ohne-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184689_-logaplus-paket-24s-gb172-14-erdgas-e-h-rc-300-sm300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3127121_-cerapurmodul-zbs-14-100-s-3-ma-14-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3092246_-logano-plus-gb-212-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2920444_-logamax-plus-gb172-14-t120-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4199466_-logaplus-paket-w30-gb172-14-t120-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2611666_-ecotherm-plus-wgb-pro-evo-15-c-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4398669_-ecocompact-vsc-146-4-5-150-14-7-kw-vaillant.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184688_-logaplus-paket-w22-gb172-14-erdgas-l-ll-rc-300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4172987_-logamax-plus-gb162-15-erdgas-e-h-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3862993_-thermo-condens-wtc-15-a-w-pea-weishaupt.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3496382_-cerapursolar-comfort-csw-14-75-3-a-31-fluessiggas-p-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3801875_-logamax-plus-gb172-14-erdgas-l-ll-15-1-kw-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3053386_-comfortline-cgw-11-100-wolf-heizsysteme.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3127825_-cerapurmodul-zbs-14-100-s-3-ma-23-erdgas-e-h-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3137614_-cerapurmodul-solar-zbs-14-210-s-3-ma-21-erdgas-l-ll-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3098335_-ecocondens-bbs-15-e-15-kw-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3094587_-hybrid-logamax-plus-gbh172-14-t75s-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2635849_-cerapur-comfort-eco-zsbe-16-3-a-23-erdgas-e-h-16-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4258562_-vitodens-343-f-11-kw-viessmann.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4202928_-logaplus-paket-w30-gb172-14-t120-erdgas-e-h-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2654412_-thermo-condens-wtc-15-a-aqua-integra-100-liter-weishaupt.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2654406_-thermo-condens-wtc-15-aw-aqua-tower-140-liter-weishaupt.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2498813_-aurocompact-vsc-s-126-3-5-180-vaillant.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1083969_-logamax-plus-gb162-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4677123_-vitodens-222-w-13-kw-viessmann.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3712883_-cerapur-comfort-eco-zsbe-16-3-a-21-erdgas-l-ll-16-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2933339_-duatron-12-elco-heating.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4206535_-logaplus-paket-w9-gb162-15-s120-rc300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4206533_-logaplus-paket-w9-gb162-15-s135rw-rc300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4280909_-logaplus-paket-k60s-gb-212-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4278868_-logaplus-paket-k59-gb-212-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4260218_-logaplus-paket-w10-gb162-15-s160rw-2-heizkreise-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4260216_-logaplus-paket-w10-gb162-15-s135rw-2-heizkreise-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184693_-logaplus-paket-w22-gb172-14-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3725813_-tzerra-15-ds-de-dietrich-remeha.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2654414_-thermo-condens-wtc-15-a-kompakt-115-liter-weishaupt.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2611680_-ecocondens-bbs-pro-evo-15-c-15-kw-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2108309_-ecosolar-bsk-15-15kw-broetje.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4215838_-logaplus-paket-w10-gb162-15-s135rw-1-heizkreis-mit-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4215836_-logaplus-paket-w10-gb162-15-s160rw-1-heizkreis-mit-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4215830_-logaplus-paket-w10-gb162-15-su160w-1-heizkreis-mit-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4215829_-logaplus-paket-w10-gb162-15-su200w-1-heizkreis-mit-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1282285_-thision-s-9-1-elco-heating.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3801860_-logamax-plus-gb172-14-erdgas-e-h-15-1-kw-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3137609_-cerapurmodul-solar-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3129273_-comfortline-csz-11-300-wolf-heizsysteme.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2933366_-duatron-solar-12-elco-heating.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4215749_-logaplus-paket-w10-why-gb162-15-su200w-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4215740_-logaplus-paket-w10-why-gb162-15-su160w-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4215727_-logaplus-paket-w10-why-gb162-15-s120-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4205989_-logaplus-paket-w41-gbh172-14-t75s-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4205800_-logaplus-paket-w31-gb172-14-t210sr-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/2920561_-logamax-plus-gb172-14-t150s-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4398673_-ecocompact-vsc-146-4-5-200-14-7-kw-vaillant.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4207237_-logaplus-paket-w9-gb162-15-su160rw-rc300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4206487_-logaplus-paket-w9s-gb162-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3935422_-cerapurmodul-zbs-14-100-s-3-ma-21-erdgas-l-ll-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4203859_-logaplus-paket-w31-gb172-14-t120-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4203844_-logaplus-paket-w31-gb172-14-t150-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4203808_-logaplus-paket-w31-gb172-14-t150s-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4203080_-logaplus-paket-w30-gb172-14-t150s-erdgas-e-h-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4202979_-logaplus-paket-w30-gb172-14-t150-erdgas-l-ll-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3725853_-calenta-15-s-de-dietrich-remeha.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3137616_-cerapurmodul-solar-zbs-14-210-s-3-ma-23-erdgas-e-h-14-2-kw-junkers.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/3131289_-vitodens-222-f-13-kw-viessmann.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1282286_-thision-s-13-1-elco-heating.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/1083985_-logano-plus-gb202-15-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4202972_-logaplus-paket-w30-gb172-14-t150-erdgas-e-h-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4202934_-logaplus-paket-w30-gb172-14-t120-erdgas-l-ll-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4202869_-logaplus-paket-w30-sr-gb172-14-t210sr-erdgas-l-ll-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4202864_-logaplus-paket-w30-sr-gb172-14-t210sr-erdgas-e-h-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4202821_-logaplus-paket-w30-sr-gb172-14-t210sr-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4199456_-logaplus-paket-w30-gb172-14-t150-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184701_-logaplus-paket-w22s-gb172-14-erdgas-e-h-rc-300-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184698_-logaplus-paket-w24s-gb172-14-erdgas-l-ll-rc-300-sm300-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184696_-logaplus-paket-w22s-gb172-14-erdgas-l-ll-rc-300-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4184692_-logaplus-paket-w22s-gb172-14-erdgas-l-ll-rc-300-ohne-mischer-buderus.html",
"http://www.idealo.de/preisvergleich/OffersOfProduct/4173011_-logamax-plus-gb162-15-erdgas-l-ll-buderus.html",

    ]

    #===========================================================================
    # def parse(self, response):
    #     for sel in response.xpath('//td'):
    #         title = sel.xpath('a/text()').extract()
    #         link = sel.xpath('a/@href').extract()
    #         desc = sel.xpath('text()').extract()
    #         print title, link, desc
    #===========================================================================

    #===========================================================================
    # def parse(self, response):
    #     for sel in response.xpath('//tr'):
    #         item = heatingItem()
    #         item['title'] = sel.xpath('td/a[@class="offer-title link-2 webtrekk"]/text()').extract()
    #         item['link'] = sel.xpath('td[@class="va-middle"]/a/@href').extract()
    #         item['pricerange'] = sel.xpath('td[@class="va-middle"]/a/span[@class="price bold nobr block fs-18"]/text()').extract()
    #        
    #         yield item
    #===========================================================================

  #  def parse(self, response):
#        for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
    #        for href in response.css("td.info >  a::attr('href')"):
    #            url = response.urljoin(href.extract())
      #          yield scrapy.Request(url, callback=self.parse_dir_contents)
  
   
    def parse_dir_contents(self, response):
        for sel in response.xpath('//tr'):
            item = heatingItem()
            item['title'] = sel.xpath('td/a[@class="offer-title link-2 webtrekk wt-prompt"]/text()').extract()
            item['price'] = sel.xpath('span[@class="price"').extract()
            yield item
