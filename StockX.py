import requests
from bs4 import BeautifulSoup
import pandas as pd
from serpapi import GoogleSearch

class StockX:

    def __init__(self):
        # Sets up variables
        self.search = input('Enter Shoe you would like to search StockX: ')
        stockX = 'site:stockx.com '
        self.search = stockX + self.search
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            }
        
        self.params = {
            'api_key': #'Get API key using serpapi.com',
             'engine': 'google',
             'q': self.search,
             'location': 'Centreville, Virginia, United States',
             'google_domain': 'google.com',
             'gl': 'us',
             'hl': 'en'
        }
        
    def web_search(self):
        #search google for sneaker within StockX site
        self.URL = GoogleSearch(self.params).get_dict()['organic_results'][0]['link']
        self.Name = self.URL.split('https://stockx.com/')
        self.Name = self.Name[1].replace('-',' ').capitalize()
        
    def web_scraper(self):
        #scrape webdata for stockX using URL
        page = requests.get(self.URL, headers=self.headers)
        soup = BeautifulSoup(page.content, "html.parser")
        self.rawData = soup.find('div', class_='chakra-container css-vp2g1e')

    def clean_data(self):
        #clean data to retrieve shoe sizes and price
        result = self.rawData.find('script').text.replace('"','').split(',')
        result = result[10:]
        self.description = []
        self.price = []
        for x in range(len(result)):
            if 'description:' in result[x]:
                self.description.append(result[x])
            if 'price:' in result[x]:
                self.price.append(result[x])
        
    def create_df(self):
        #store sneaker price and size data into dataframe
        df = pd.DataFrame(list(zip(self.description, self.price)), columns = ['Size','Price'])
        df['Size'] = df['Size'].str.replace('description:','')
        df['Price'] = df['Price'].str.replace('price:','')
        self.df = df.to_string(index=False)

    def main(self):
        self.web_search()
        self.web_scraper()
        self.clean_data()
        self.create_df()
        print(self.Name)
        print(self.df)
    
A = StockX()
A.main()