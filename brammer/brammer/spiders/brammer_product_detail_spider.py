# -*- coding: utf-8 -*-
"""
Created on June 21, 2019
@author: Stacy Bridges
# scrape product info
# rem disable follow robot.txt
"""

# imports  =========================================
import scrapy
import csv

# globals  =========================================
global headerRowExists
headerRowExists = False

# classes  =========================================
class BrammerProductDetail_Spider(scrapy.Spider):
    name = "BrammerProductDetail"

    start_urls = [
            "https://uk.brammer.biz/category/980/Circular-Buffers/products",
    ]

    def parse(self, response):
        # get list of product-level links
        lnk_lst = response.css('div.itemNameBox a::attr(href)').getall()

        # update product-level product links to contain full https:// path
        i = 0
        for link in lnk_lst:
            link = 'https://uk.brammer.biz' + link
            lnk_lst[i] = link
            i += 1

        # get product names to go with the list
        # prd_nm_lst = response.css('div.itemNameBox a::attr(title)').getall()

        # start a dictionary to store your results
        # product_details = {}

        # for each product link, go scrape the product details
        i = 0
        for link in lnk_lst:
            print('\n\ncalling get_prd_details\n\n')  # test
            print(link)  # test

            yield scrapy.Request(link, callback=self.get_prd_details)
            i += 1
        # end function //


    def get_prd_details(self, response):
        global headerRowExists

        print('\n\ngetting product details\n\n')  # test

        product = response.css('div.product-info h2::text').get()
        base = response.css('table.cpn-synonims-table')
        sku = base.css('span::text').get()
        brand = base.css('a::text').get()
        mpn_base = response.css('table.cpn-synonims-table tr td')[5]
        mpn = mpn_base.css('::text').get()

        # attr paths
        base3 = response.css('div.tabs-wrapper ul.tabs-content li div.product_data_detail_row_even')
        attr_key = base3.css('div.product_data_detail_row_label::text').getall()  # get list of attr keys
        attr_val = base3.css('div.product_data_detail_row_value::text').getall()  # get list of attr vals

        # put attributes into an attribute dictionary
        attr = {}
        j = 0
        for k in attr_key:
            attr[attr_key[j]] = attr_val[j]
            j += 1

        with open('test.csv', mode = 'a') as outfile:
            writer = csv.writer(outfile, delimiter = '|',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if headerRowExists == False:
                writer.writerow(['Product', 'SKU', 'Brand', 'MPN', 'Attr'])
                headerRowExists = True
            writer.writerow([product.strip(), sku, brand, mpn, attr])
        '''
        return {
            'Product': product,
            'SKU': sku,
            'Brand': brand,
            'MPN': mpn,
            'attr': attr
        }
        '''
        # end function //
