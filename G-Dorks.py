#! /usr/bin/env python3 
import sys
import requests
from bs4 import BeautifulSoup
import argparse
import cmd
import logging
import GoogleDorks
logging.basicConfig(filename='G-Dorks.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
dorks = [
        "()", "*", "\"\"", "m..n", "-", "+", "|", "~", "@", "after", "allintitle", "allinurl",
        "allintext", "AROUND", "author", "before", "cache", "contains", "date", "define", "ext",
        "filetype", "inanchor", "index", "info", "intext", "intitle", "inurl", "link", "location",
        "numrange", "OR", "phonebook", "relate", "safesearch", "source", "site", "stock", "weather"
    ]  


class GoogleDorksShell(cmd.Cmd):
    intro = "Welcome to G-Dorks. Type help or ? to list commands.\n"
    prompt = "G-Dorks>> "

    def do_ad(self, arg):
        """Display available dorks."""
        GoogleDorks.display_available_dorks()

    def do_hh(self, arg):
        """Display detailed help menu."""
        print("Detailed help menu:")
        GoogleDorks.display_detailed_help_menu()
    
    def do_search_single_dork(self, arg):
        """Search Google with given single keywords or single dork."""
        args = arg.split()
        if len(args) >= 2:
            search_keyword = ' '.join(args[1:])
            if args[0] in GoogleDorks.dorks:
                search_query = f"{args[0]}:" 
            else:
                search_query = args[0] + ":" + search_keyword
            results = GoogleDorks.search_google_dork(search_query)
            if results:
                print("Search results:")
                for idx, result in enumerate(results, start=1):
                    print(f"{idx}. {result}")
            else:
                print("No search results found.")
        else:
            print("Please provide keywords or a dork to search.")
    
    def do_search_with_what_do_you_want_with_dorks(self, arg):
        """Search Google with given with what do you want. Example: search inurl:pastebin intitle:mastercard """
        args = arg.split()
        if len(args) >= 2:
            query = args[0]
            start = args[1]
            print("Results:", GoogleDorks.search_google_dorks(query, start))
        else:
            print("Please provide query and start index.")
        
    def do_quit(self, arg):
        """Exit the shell."""
        print("Exiting G-Dorks.")
        return True

def main():
    # Start the custom interactive shell
    GoogleDorksShell().cmdloop()

if __name__ == "__main__":
    main()