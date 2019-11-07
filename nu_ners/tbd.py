import generate_mpn_patterns_2
import extract_brands_ners_adhoc
import http.server
import socketserver
import os, sys

def main():
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

if __name__ == '__main__' : main()
