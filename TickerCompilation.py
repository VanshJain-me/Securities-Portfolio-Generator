#!/usr/bin/env python3

# TickerCompilation.py

# AUTHOR: Vansh Jain
# HANDLE: VanshJain-me
# Compiles the company names and thier tickers from ADVFN

####
# Add random time to prevent DOS
# ADD logging and other software development htings

import pandas as pd

import requests
from bs4 import BeautifulSoup

import string


"""
Scrape the data from ADVEN, structure, format and clean
the data
"""


class TickerCompilation:

    """
    Definition of objects
    """

    def __init__(self):

        self.URLS = [
            "https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=",
            "https://www.advfn.com/nasdaq/nasdaq.asp?companies=",
            "advfn.com/amex/americanstockexchange.asp?companies=A",
        ]
        self.EXCHANGES = ["NYSE", "NASDAQ", "AMEX"]
        self.HEADERS = ["Security's Name", "Ticker", "Exchange"]

        self.url = ""
        self.exchange = ""

        self.link = ""
        self.name = []
        self.ticker = []
        self.exchange_list = []

        self.data

    """
    Formats the URL to get the required webpage
    """

    def url_formatter(self, character):

        self.link = self.url + character

    """
    Filters the data from the parsed text and stores it
    """

    def get_data(self, rows):

        for row in rows:
            data = row.find_all("td")
            self.name.append(data[0].text.strip())
            self.ticker.append(data[1].text.strip())
            self.exchange_list.append(self.exchange)

    """
    Scrapes the data off the webpage
    """

    def web_scraper(self):

        page = requests.get(self.link)
        soup = BeautifulSoup(page.text, "html.parser")

        odd_rows = soup.find_all("tr", attrs={"class": "ts0"})
        even_rows = soup.find_all("tr", attrs={"class": "ts1"})

        self.get_data(odd_rows)
        self.get_data(even_rows)

    """
    Formats and structures the data
    """

    def data_format(self):

        self.data = pd.DataFrame(columns=self.HEADERS)
        self.data["Issuing Entity"] = self.name
        self.data["Ticker"] = self.ticker
        self.data["Exchange"] = self.exchange_list

    """
    Cleans the data by removing empty columns
    """

    def data_cleaning(self):

        self.data = self.data[self.data["Issuing Entity"] != ""]

    """
    Stores the data on ROM in CSV format
    """

    def data_store(self):
        self.data.to_csv("/data/tickers/tickers.csv")

    """
    Compiles the list of tickers and structures, formats
    and stores the data
    """

    def compile(self):
        for element in range(len(self.URLS)):
            self.url = self.URLS[element]
            self.exchange = self.EXCHANGES[element]

            for character in string.ascii_uppercase:
                self.url_formatter(character)
                print(self.link)
                self.web_scraper()

        self.data_format()
        self.data_cleaning()
        self.data_store()

        self.data.head()


def main():
    compilationObj = TickerCompilation()
    compilationObj.compile()


if __name__ == "__main__":
    main()
