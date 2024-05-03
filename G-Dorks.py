import sys
import argparse
import logging
import urllib.parse
import urllib.request
import time
import json
from urllib.parse import urlparse

banner = """ 
 .d8888b.         8888888b.                   888               
d88P  Y88b        888  "Y88b                  888               
888    888        888    888                  888               
888               888    888  .d88b.  888d888 888  888 .d8888b  
888  88888        888    888 d88""88b 888P"   888 .88P 88K      
888    888 888888 888    888 888  888 888     888888K  "Y8888b. 
Y88b  d88P        888  .d88P Y88..88P 888     888 "88b      X88 
 "Y8888P88        8888888P"   "Y88P"  888     888  888  88888P' 
                                                                
                                                                
             v1  made by 0xcybersoldier 
"""


domain = ''
engine = ''
key = ''
max_queries = 10
sleep = 0
dynamic_filetypes = "html,htm,asp,aspx,cfm,cgi,jsp,php5,php,phtm,phtml,shtm,shtml,XHTML,RSS,XPS"

class Functions:
    @staticmethod
    def display_available_dorks():
        dorks = [
            "()", "*", "\"\"", "m..n", "-", "+", "|", "~", "@", "after", "allintitle", "allinurl",
            "allintext", "AROUND", "author", "before", "cache", "contains", "date", "define", "ext",
            "filetype", "inanchor", "index", "info", "intext", "intitle", "inurl", "link", "location",
            "numrange", "OR", "phonebook", "relate", "safesearch", "source", "site", "stock", "weather"
        ]
        print("Available dorks:")
        for dork in dorks:
            print(dork)

    @staticmethod
    def display_detailed_help_menu():
        help_menu = """
    ():    Group multiple terms or operators. Allows advanced expressions    (<term> or <operator>)    inurl:(html | php)
    *:    Wildcard. Matches any word    <text> * <text>    How to * a computer
    "":    The given keyword has to match exactly. case-insensitive    "<keywords>"    "google"
    m..n / m...n:    Search for a range of numbers. n should be greater than m    <number>..<number>    1..100
    -:    Documents that match the operator are excluded. NOT-Operator    -<operator>    -site:youtube.com
    +:    Include documents that match the operator    +<operator>    +site:youtube.com
    |:    Logical OR-Operator. Only one operator needs to match in order for the overall expression to match    <operator> | <operator>    "google" | "yahoo"
    ~:    Search for synonyms of the given word. Not supported by Google    ~<word>    ~book
    @:    Perform a search only on the given social media platform. Rather use site    @<socialmedia>    @instagram
    after:    Search for documents published / indexed after the given date    after:<yy(-mm-dd)>    after:2020-06-03
    allintitle:    Same as intitle but allows multiple keywords seperated by a space    allintitle:<keywords>    allintitle:dog cat
    allinurl:    Same as inurl but allows multiple keywords seperated by a space    allinurl:<keywords>    allinurl:search com
    allintext:    Same as intext but allows multiple keywords seperated by a space    allintext:<keywords>    allintext:math science university
    AROUND:    Search for documents in which the first word is up to n words away from the second word and vice versa    <word1> AROUND(<n>) <word2>    google AROUND(10) good
    author:    Search for articles written by the given author if applicable    author:<name>    author:Max
    before:    Search for documents published / indexed before the given date    before:<yy(-mm-dd)>    before:2020-06-03
    cache:    Search on the cached version of the given website. Uses Google's cache to do so    cache:<domain>    cache:google.com
    contains:    Search for documents that link to the given fileype. Not supported by Google    contains:<filetype>    contains:pdf
    date:    Search for documents published within the past n months. Not supported by Google    date:<number>    date:3
    define:    Search for the definition of the given word    define:<word>    define:funny
    ext:    Search for a specific filetype    ext:<documenttype>    ext:pdf
    filetype:    Refer to ext    filetype:<documenttype>    filetype:pdf
    inanchor:    Search for the given keyword in a website's anchors    inanchor:<keyword>    inanchor:security
    index of:    Search for documents containing direct downloads    index of:<term>    index of:mp4 videos
    info:    Search for information about a website    info:<domain>    info:google.com
    intext:    Keyword needs to be in the text of the document    intext:<keyword>    intext:news
    intitle:    Keyword needs to be in the title of the document    intitle:<keyword>    intitle:money
    inurl:    Keyword needs to be in the URL of the document    inurl:<keyword>    inurl:sheet
    link / links :    Search for documents whose links contain the given keyword. Useful for finding documents that link to a specific website    link:<keyword>    link:google
    location:    Show documents based on the given location    location:<location>    location:USA
    numrange:    Refer to m..n    numrange:<number>-<number>    numrange:1-100
    OR:    Refer to |    <operator> OR <operator>    "google" OR "yahoo"
    phonebook:    Search for related phone numbers associated with the given name    phonebook:<name>    phonebook:"william smith"
    relate / related:    Search for documents that are related to the given website    relate:<domain>    relate:google.com
    safesearch:    Exclude adult content such as pornographic videos    safesearch:<keyword>    safesearch:sex
    source:    Search on a specific news site. Rather use site    source:<news>    source:theguardian
    site:    Search on the given site. Given argument might also be just a TLD such as com, net, etc    site:<domain>    site:google.com
    stock:    Search for information about a market stock    stock:<stock>    stock:dax
    weather:    Search for information about the weather of the given location    weather:<location>    weather:Miami
"""
        print(help_menu)

def search_google_dorks(domain, engine, key, max_queries, sleep, dynamic_filetypes, terms, output_file=None):
    if not key or not engine:
        print("ERROR: [key] and [engine] must be set", file=sys.stderr)
        return

    data = {}
    data['key'] = key
    data['cx'] = engine
    data['siteSearch'] = domain
    data['q'] = ' '.join(terms)
    if dynamic_filetypes:
        filetypes = dynamic_filetypes.split(',')
        data['q'] += ' filetype:' + ' OR filetype:'.join(filetypes)
    data['num'] = 10
    data['start'] = 1

    pages = set()
    found = 0
    query_max_reached = False
    query_count = 0
    data_saved = data['q']

    results = []

    while query_count < max_queries:
        url = 'https://www.googleapis.com/customsearch/v1?' + urllib.parse.urlencode(data)
        try:
            response_str = urllib.request.urlopen(url)
            query_count += 1
            response_str = response_str.read().decode('utf-8')
            response = json.loads(response_str)
        except urllib.error.HTTPError as e:
            response_str = e.read().decode('utf-8')
            response = json.loads(response_str)
            if "Invalid Value" in response['error']['message']:
                return results
            elif response['error']['code'] == 500:
                data['q'] = data_saved
                query_max_reached = True
                continue
            print("error: " + str(response['error']['code']) + " - " + str(response['error']['message']), file=sys.stderr)
            for error in response['error']['errors']:
                print(error['domain'] + "::" + error['reason'] + "::" + error['message'], file=sys.stderr)
            if "User Rate Limit Exceeded" in response['error']['message']:
                print("sleeping " + str(sleep) + " seconds", file=sys.stderr)
                time.sleep(5)
            elif sleep and "Daily Limit Exceeded" in response['error']['message']:
                print("sleeping " + str(sleep) + " seconds", file=sys.stderr)
                time.sleep(sleep)
                continue
            else:
                return results
        data_saved = data['q']
        for request in response['queries'].get('request', []):
           if 'totalResults' in request and int(request['totalResults']) == 0:
                return results

        for item in response['items']:
            item_url = urlparse(item['link'])
            if item_url.path in pages:
                if not query_max_reached:
                    data['q'] += " -inurl:" + item_url.path
            else:
                pages.add(item_url.path)
                found += 1
                results.append(item['link'])
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(item['link'] + '\n')
        if found >= data['num'] or query_max_reached:
            data['start'] += data['num']
    return results

def main():
    print(banner)
    parser = argparse.ArgumentParser(description='Find dynamic pages via G-Dorks in Google Search Engine.')
    
    # Create an argument group for search functionality
    search_group = parser.add_argument_group('Search Options', 'Options for search functionality')
    
    # Add options within the search group
    search_group.add_argument('--dorks', action='store_true', help='Display available dorks')
    search_group.add_argument('--detailed_dorks', action='store_true', help='Display detailed dorks')
    search_group.add_argument('-o', '--output', required=False, help='File to save the results')
    search_group.add_argument('-l', '--log', required=False, default='G-Dorks.log', help='File to save the logs')
    
    # Add options outside the search group
    parser.add_argument('-d', '--domain', required=not any(arg in sys.argv for arg in ['--dorks', '--detailed_dorks']), help='Specific domain to search (instead of all domains defined in CSE)')
    parser.add_argument('-e', '--engine', required=not any(arg in sys.argv for arg in ['--dorks', '--detailed_dorks']), help='Google custom search engine id (cx value)')
    parser.add_argument('-k', '--key', required=not any(arg in sys.argv for arg in ['--dorks', '--detailed_dorks']), help='Google API key')
    parser.add_argument('-m', '--max-queries', type=int, default=10, help='Maximum number of queries to issue')
    parser.add_argument('-s', '--sleep', type=int, default=0, help='Seconds to sleep before retry if daily API limit is reached (0=disable)')
    
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(filename=args.log, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    if args.dorks:
        Functions.display_available_dorks()
    elif args.detailed_dorks:
        Functions.display_detailed_help_menu()
    else:
        results = search_google_dorks(args.domain, args.engine, args.key, args.max_queries, args.sleep, dynamic_filetypes, [], args.output)
        if results:
            print("Results:")
            for result in results:
                print(result)
        else:
            print("No results found.")

if __name__ == "__main__":
    main()
