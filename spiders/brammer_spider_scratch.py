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
            'https://uk.brammer.biz/',
    ]

    def parse(self, response):
        # get list of group-level links from home page
        grp_lnk_lst = response.css('div.prod-box div.texts a::attr(href)').getall()

        # update group-level product links to contain full https:// path
        grp_lnk_lst = get_full_length_path(grp_lnk_lst)


        # follow each link in the list of  group-level product links
        for link in grp_lnk_lst:
            request = scrapy.Request(link, callback=self.follow_grp_lnk)
            yield = request
            #
            # PROCESS REQUEST
            #

        # end function //

    def follow_grp_lnk(self, response):
        # if the link points to a product-level page,
        # use dom path to scrape a product page
        if response.request.url.find('/product') > 0:
            # get list of product-level links
            prd_lnk_lst = response.css('div.itemNameBox a::attr(href)').getall()

            # update product-level product links to contain full https:// path
            prd_lnk_lst = get_full_length_path(prd_lnk_lst)

            for link in prd_lnk_lst:
                request = scrapy.Request(link, callback=self.get_prd_details)
                yield = request
                #
                # PROCESS REQUEST
                #

        else:
            # do something related to the grp lnk

        # end function //

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
        attr_dict = {}

        for

        yield {
        prod_key : prod_val,
        itemno_key: itemno_val,
        brand_key: brand_val,
        mpn_key: mpn_val,
        attr_dict
        }

        # end function //
