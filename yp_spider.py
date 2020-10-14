# -*- coding: utf-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|r|e|d|a|n|d|g|r|e|e|n|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


import scrapy
import os
from scrapy.crawler import CrawlerProcess
from scrapy import Request

class YellowPages(scrapy.Spider):

    name = 'yellow-pages'
    custom_settings = { 'FEEDS':{'results.csv' : { 'format' : 'csv'}}}
    start_urls = ['https://www.yellowpages.com.au/search/listings?clue=accountants&locationClue=nwz&lat=&lon=']
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        
    try:
        os.remove('results.csv')
    except OSError:
        pass
        
    def parse(self, response):

        listings = response.xpath('//*[@class="listing listing-search listing-data"]')
        for card in listings:
            listing_name = card.xpath('.//*[@class="listing-name"]/@href').get()
            opening_time = card.xpath('.//span[@class="from-time"]/text()').get()
            closing_time = card.xpath('.//span[@class="to-time"]/text()').get()
            website = card.xpath('.//*[@class="contact contact-main contact-url "]/@href').get()
            
            items = {
                'name' : listing_name,
                'opening_time' : opening_time,
                'closing_time' : closing_time,
                'website' : website
                
            }
            
            
            yield items

        if response.xpath('//a[contains(text(), "Next »")]'):
            next_url= response.xpath('//a[contains(text(), "Next »")]/@href').get().replace('&referredBy=UNKNOWN','')
            
            # got to next page, until no more 'next'
            
            yield response.follow(next_url, callback=self.parse)
        
         
         
# -- main driver --

if __name__ == "__main__" :
    process= CrawlerProcess()
    process.crawl(YellowPages)
    process.start()
        
       
