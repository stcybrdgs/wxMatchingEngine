# -*- coding: utf-8 -*-
"""
Created on June 21, 2019
@author: Stacy Bridges
# scrape product info
# rem disable follow robot.txt
"""

'''
"https://uk.brammer.biz//category/113/Polyurethane-V-Belts/products",
"https://uk.brammer.biz//category/1075/Overload-Relays/products",
"https://uk.brammer.biz//category/1076/Switches-Push-Buttons-Indicators/products",
"https://uk.brammer.biz//category/1077/Limit-Switches/products",
"https://uk.brammer.biz//category/1050/Electronic-Timers-Counters/products",
"https://uk.brammer.biz//category/1057/Encoders-Resolvers-Tacho-39-s/products",
"https://uk.brammer.biz//category/1116/Lamps/products",
"https://uk.brammer.biz//category/1117/Tubes/products",
"https://uk.brammer.biz//category/1112/Sensor-Accessories/products",
"https://uk.brammer.biz//category/244/Valve-Islands/products",
"https://uk.brammer.biz//category/245/Multiple-valves/products",
"https://uk.brammer.biz//category/254/Shuttle-Valves/products",
"https://uk.brammer.biz//category/255/Ball-Valves/products",
"https://uk.brammer.biz//category/258/Logic-valves/products",
"https://uk.brammer.biz//category/259/Timer-Valves/products",
"https://uk.brammer.biz//category/260/Two-hand-Control/products",
"https://uk.brammer.biz//category/277/Plate-Actuators/products",
"https://uk.brammer.biz//category/279/Pin-Actuators/products",
"https://uk.brammer.biz//category/285/Bellows-Actuators/products",
"https://uk.brammer.biz//category/298/Pneumatic-Actuator-with-Linear-Guide-Units/products",
"https://uk.brammer.biz//category/313/Drain-Separator/products",
"https://uk.brammer.biz//category/315/Air-Dryers/products",
"https://uk.brammer.biz//category/334/Piping/products",
"https://uk.brammer.biz//category/339/Vacuum-Switches/products",
"https://uk.brammer.biz//category/344/Vacuum-Accessories/products",
"https://uk.brammer.biz//category/367/Flow-Valves-Standard-/products",
"https://uk.brammer.biz//category/368/Directional-Control-Valves-Standard-/products",
"https://uk.brammer.biz//category/410/Internal-Gear-Pumps/products",
"https://uk.brammer.biz//category/412/Hand-Pumps/products",
"https://uk.brammer.biz//category/380/Single-Rod-Cylinders/products",
"https://uk.brammer.biz//category/383/Pressure-Filters/products",
"https://uk.brammer.biz//category/384/Return-Filters/products",
"https://uk.brammer.biz//category/386/Suction-Filters/products",
"https://uk.brammer.biz//category/387/Filter-Assemblies/products",
"https://uk.brammer.biz//category/397/Diaphragm-Accumulators/products",
"https://uk.brammer.biz//category/399/Accumulator-Accessories/products",
"https://uk.brammer.biz//category/406/Pipe-Clips-Clamps/products",
"https://uk.brammer.biz//category/74650/Ball-Valves/products",
"https://uk.brammer.biz//category/74672/Positive-Displacement-Pumps/products",
"https://uk.brammer.biz//category/74676/Submersible-Pumps/products",
"https://uk.brammer.biz//category/74677/Drum-Barrel-Pumps/products",
"https://uk.brammer.biz//category/74680/Process-Pumps-Others/products",
"https://uk.brammer.biz//category/74688/Air-Filters/products",
"https://uk.brammer.biz//category/74691/Process-Filtration-Assemblies/products",
"https://uk.brammer.biz//category/74693/Process-Filtration-Cartridges-Elements/products",
"https://uk.brammer.biz//category/74697/Industrial-Rubber-Hose/products",
"https://uk.brammer.biz//category/74698/Suction-and-Delivery-Hose/products",
"https://uk.brammer.biz//category/74699/Layflat-Hose/products",
"https://uk.brammer.biz//category/74700/Industrial-Thermoplastic-Hose/products",
"https://uk.brammer.biz//category/74719/Rotary-Joints-Unions/products",
"https://uk.brammer.biz//category/74724/Connectors-Fittings-Couplings-Sealing-Washers/products",
"https://uk.brammer.biz//category/74547/Pressure-Transmitters/products",
"https://uk.brammer.biz//category/74548/Pressure-Measurement-Others/products",
"https://uk.brammer.biz//category/74549/Flow-Switches-Sensors/products",
"https://uk.brammer.biz//category/74550/Flow-Measurement-Others/products",
"https://uk.brammer.biz//category/448/Brad-Point/products",
"https://uk.brammer.biz//category/458/Others-Reamers/products",
"https://uk.brammer.biz//category/482/Others-Indexable-Cutting-Tips/products",
"https://uk.brammer.biz//category/527/Others-Hand-Saws-and-Blades/products",
"https://uk.brammer.biz//category/586/Measures/products",
"https://uk.brammer.biz//category/643/Fans-and-Air-Cooling/products",
"https://uk.brammer.biz//category/644/Others-Heating-Ventilation/products",
"https://uk.brammer.biz//category/696/Others-Fall-Protection-Arrest/products",
"https://uk.brammer.biz//category/71074/Prescription-Eyewear/products",
"https://uk.brammer.biz//category/718/Podiums-Platforms/products",
"https://uk.brammer.biz//category/719/Towers/products",
"https://uk.brammer.biz//category/720/Height-Access-Equipment-Accessories/products",
"https://uk.brammer.biz//category/721/Others-Height-Access-Equipment/products",
"https://uk.brammer.biz//category/730/Belts/products",
"https://uk.brammer.biz//category/1009/Silane-Modified-Polymers/products",
'''

# imports  =========================================
import scrapy

# helpers  =========================================
def get_full_link_path(lnk_lst):
    nu_list = []
    for link in lnk_lst:
        link = 'https://uk.brammer.biz' + link
        nu_list.append(link)
    lnk_lst.clear()
    return nu_list

# classes  =========================================
class Brammer_Spider(scrapy.Spider):
    name = "Brammer"
    start_urls = [
            "https://uk.brammer.biz//category/980/Circular-Buffers/products",
    ]

    def parse(self, response):
        # get list of product-level links
        prd_lnk_lst = response.css('div.itemNameBox a::attr(href)').getall()

        # update product-level product links to contain full https:// path
        prd_lnk_lst = get_full_length_path(prd_lnk_lst)

        # get product names to go with the list
        prd_nm_lst = response.css('div.itemNameBox a::attr(title)').getall()

        # start a dictionary to store your results
        product_details = {}

        # for each product link, go scrape the product details
        i = 0
        for link in prd_lnk_lst:
            request = scrapy.Request(link, callback=self.get_prd_details)
            product_details[prd_nm_lst[i]] = request
            i += 1

        yield product_details

    def get_prd_details(self, response):
        # product path
        base = response.css('div.product-info')
        prod_key = 'product'
        prod_val = base.css('h2::attr(data-name)').get()

        # product id path
        base2 = base.css('table.cpn-synonims-table')
        itemno_key = 'product id'
        itemno_val = base2.css('tr td span::text').get()

        # brand path
        brand_key = 'brand'
        brand_val = base2.css('tr td a::text').get()

        # key path
        mpn_key ='mpn'
        mpn_val_base = base2.css('tr')[2]
        mpn_val = mpn_val_base.css('td::text')[1].get()

        # attr paths
        base3 = response.css('div.tabs-wrapper ul.tabs-content li div.product_data_detail_row_even')
        attr_key = base3.css('div.product_data_detail_row_label::text').getall()  # get list of attr keys
        attr_val = base3.css('div.product_data_detail_row_value::text').getall()  # get list of attr vals

        # put attributes into an attribute dictionary
        attr = {}
        i = 0
        for k in attr_key:
            attr[attr_key[i]] = attr_val[i]
            i += 1

        yield {
            prod_key: prod_val,
            itemno_key: itemno_val,
            brand_key: brand_val,
            mpn_key: mpn_val,
            'attr': attr
        }

        # end function //
