import generate_mpn_patterns_2
import extract_brands_ners_adhoc
import http.server
import socketserver
import os, sys
import compute_wbrand_primary
import extract_rs_codes

def main():
    '''
    print('\nThis function is under development.')
    #extract_brands_ners_adhoc.main('ners_db_brands_wx_patterns.jsonl','mpn_tender.csv')
    #generate_mpn_patterns_2.main('db_mpn_delme_test')

    folder_path = os.path.dirname(os.path.abspath(__file__))
    http_ = folder_path + '\\' + 'displacy\\index.html'
    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


    brands = ['one', 'two', 'one hundred','six', 'three']
    counts = [1, 2, 100, 6, 3]
    index_of_max_count = counts.index(max(counts))
    prim_brand = brands[index_of_max_count]
    print(prim_brand)
    '''

    file_name = 'db_data_org_electrical_nutest_wx_v1.xlsx'
    extract_rs_codes.main(file_name, 'LongText')

if __name__ == '__main__' : main()
