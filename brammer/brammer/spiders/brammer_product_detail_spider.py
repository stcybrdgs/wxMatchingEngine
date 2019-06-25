# -*- coding: utf-8 -*-
"""
Created on June 24, 2019
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
    headerRowExists = False

    start_urls = [
            "https://uk.brammer.biz/category/65/Metallic-Bearing-Seals/products",
            "https://uk.brammer.biz/category/980/Circular-Buffers/products",
            "https://uk.brammer.biz/category/980/Circular-Buffers/products",
            "https://uk.brammer.biz/category/113/Polyurethane-V-Belts/products",
            "https://uk.brammer.biz/category/1066/AC-Variable-Speed-Drives-Accessories/products",
            "https://uk.brammer.biz/category/1075/Overload-Relays/products",
            "https://uk.brammer.biz/category/1077/Limit-Switches/products",
            "https://uk.brammer.biz/category/1050/Electronic-Timers-Counters/products",
            "https://uk.brammer.biz/category/1117/Tubes/products",
            "https://uk.brammer.biz/category/244/Valve-Islands/products",
            "https://uk.brammer.biz/category/258/Logic-valves/products",
            "https://uk.brammer.biz/category/368/Directional-Control-Valves-Standard-/products",
            "https://uk.brammer.biz/category/74672/Positive-Displacement-Pumps/products",
            "https://uk.brammer.biz/category/74676/Submersible-Pumps/products",
            "https://uk.brammer.biz/category/74677/Drum-Barrel-Pumps/products",
            "https://uk.brammer.biz/category/74680/Process-Pumps-Others/products",
            "https://uk.brammer.biz/category/448/Brad-Point/products",
            "https://uk.brammer.biz/category/473/Others-HoleSaws/products",
            "https://uk.brammer.biz/category/643/Fans-and-Air-Cooling/products",
            "https://uk.brammer.biz/category/730/Belts/products",
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

        # for each product link, go scrape the product details
        i = 0
        for link in lnk_lst:
            yield scrapy.Request(link, callback=self.get_prd_details)
            i += 1

        # end function //

    def get_prd_details(self, response):
        global headerRowExists

        # get a product hash id
        hashid_base = response.css('div.product-info h2::attr(data-category)').get()
        hashid = hashid_base[hashid_base.rfind('(')+1:len(hashid_base)-1]

        # get product, sku, brand, and mpn
        product = response.css('div.product-info h2::text').get()
        base = response.css('table.cpn-synonims-table')
        sku = base.css('span::text').get()
        brand = base.css('a::text').get()
        mpn_base = response.css('table.cpn-synonims-table tr td')[5]
        mpn = mpn_base.css('::text').get()

        # get product attributes (if any)
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
            writer = csv.writer(outfile,
                                delimiter = '|',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            if headerRowExists == False:
                writer.writerow(['HashID', 'Product', 'SKU', 'Brand', 'MPN', 'Attr'])
                headerRowExists = True
            writer.writerow([hashid, product.strip(), sku, brand, mpn, attr])

        # end function //
