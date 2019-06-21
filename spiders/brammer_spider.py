# -*- coding: utf-8 -*-
"""
Created on June 21, 2019
@author: Stacy Bridges
# scrape product info
# rem disable follow robot.txt
"""

# imports  =========================================
import scrapy


# classes  =========================================
class Brammer_Spider(scrapy.Spider):
    name = "Brammer"
    start_urls = [
            'https://uk.brammer.biz/',
    ]

    def parse(self, response):
        # get the set of group-level product links from the home page
        group_link_list = response.css('div.prod-box div.texts a::attr(href)').getall()

        grp_lnk_lst = []  # this will be our master set of group-level links
        for link in group_link_list:
            link = 'https://uk.brammer.biz' + link
            grp_lnk_lst.append(link)

        group_link_list.clear()

        for link in grp_lnk_lst:
            request = scrapy.Request(link, callback=self.get_next_link_list)
            cat_lnk_lst = yield request

        def get_next_link_list():
            pass


        #i = 0
        for item in productListItem:
            yield {
                    'ProductName' : item.css('h4 a::text').get(),
                    'OrderCode' : item.css('ul.list-view__details li strong::text')[0].get(),
                    'Brand' : item.css('ul.list-view__details li strong::text')[1].get(),
                    'MfrPartNo' : item.css('ul.list-view__details li strong::text')[2].get(),
            }


# main     =========================================
def main():
	print('Done.')

if __name__ == '__main__': main()
