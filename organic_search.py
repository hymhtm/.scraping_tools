import os
import random
import requests
import time

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pandas as pd

def __init__(self):
    load_dotenv()
    self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    self.CX = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    self.SEARCH_API_URL = "https://www.googleapis.com/customsearch/v1"
    self.delay = random.uniform(1,3) #random delay between requests



def google_search(self, query):
    """search something using Googl Custom Search JSON API"""

    params = {
        'q': query,
        'key': self.GOOGLE_API_KEY,
        'cx': self.CX,
        'c2coff': 0.8, #confidence level
        'cr': 'countryJP', #country restriction
        'enableAlternateSearchHandler': True,
        'filter': 1, #filter for duplicate content
        'gl': 'jp', #country of user
        'lr': 'lang_ja', #language
        'num': 3, #number of results per page
        'safe': 'active', #safe search
    }
    
    try:
        response = requests.get(self.SEARCH_API_URL, params=params)
        response.raise_for_status()
        results = response.json().get('items', [])
        
        if not results:
            print(f"No results found for {query}")
        
        elif results:
            return results[0]['link']
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"Search API Error: {e}")
        return None
    
    except KeyError:
        print(f"Unexpected API response structure for {query}")
        return None
    

def extract_href_text(soup):
    """extract href text from a given soup object"""
    href_texts = []
    for a_tag in soup.find_all('a', href=True):
        href_texts.append(a_tag.text.strip())
    return href_texts


def scrape_company_info(self, url):
    """scrape company infromation from a given url"""


    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = {
            'company_url': url,
            'company_name': extract_company_name(soup),
            'company_postal_code': extract_postal_code(soup),
            'company_address': extract_japan_address(soup),
            'company_phone': extract_phone(soup),
            'company_email': extract_email(soup),
            'employee_count': extract_employee_count(soup),
            'capital': extract_capital(soup),
            'financial_status': extract_financial_status(soup),
            'contact_form': find_contact_form(soup, url),
        }
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Scraping Error: {e}")
        return None
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None