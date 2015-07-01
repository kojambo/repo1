import scrapy.cmdline

def main():
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'heating','-o items.csv'])

if  __name__ =='__main__':
    main()