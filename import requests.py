import json
import random
import requests
import re
import time

from bs4 import BeautifulSoup
import pandas as pd

def __init__(self):
    self.GOOGLE_API_KEY = "YOUR_API_KEY"
    self.CX = "YOUR_CX"
    self.SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"
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
    
def extract_company_name(soup):
    """extract company name from a given soup object"""
    return soup.find('title').text.strip()
    
def extract_postal_code(soup):
    """extract postal code from a given soup object"""
    postal_code_pattern = re.compile(r'\d{3}-\d{4}')

def postal_search(postalcode):
    """search postal code from a given postal code
    How to use:
    prefecture = data['addresses'][0]['ja']['prefecture']
    city = data['addresses'][0]['ja']['address1']
    town = data['addresses'][0]['ja']['address2']
    address3_ja = data['addresses'][0]['ja']['address3']
    
    Args:
        postalcode(str or int): postal code
    Returns:
        json: postal code data
        None: if API search error
    
    Reference: https://github.com/ttskch/jp-postal-code-api
    """

    if type(postalcode) == str:
        postalcode = postalcode.replace('-', '')
    else:
        postalcode = postalcode
    
    #API search
    url = f"https://jp-postal-code-api.ttskch.com/api/v1/{postalcode}.json"
    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"API検索エラー: {response.status_code}")
        return None

def extract_japan_address(soup):
    """extract japan address from a given soup object"""

    jp_pref_city_pattern = re.compile(
        r'(...??[都道府県])(.+?郡.+?[町村]|.+?市.+?区|.+?[市区町村])(.+)'
    )  
    jp_address_pattern = re.compile(
        r'(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村)市|.+?郡(?:玉村|大町|.+?)[町村]|.+?市.+?区|.+?[市区町村])(.+)'
    )
    
    for text in soup.stripped_strings:
        address_match = jp_address_pattern.search(text)
        if address_match:
            return address_match.group(1).strip()
    else:
        return None
    
def extract_phone(soup):
    """extract phone number from a given soup object"""
    phone_pattern = re.compile(r'\d{2,4}-\d{2,4}-\d{4}')
    return soup.find(string=phone_pattern)

def extract_email(soup):
    """extract email from a given soup object"""
    email_pattern = re.compile(r'[a-zA-Z-0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    return soup.find(string=email_pattern)


def extract_employee_count(soup):
    """extract employee count from a given soup obejct"""
    employee_keywords = ["社員数","従業員数","従業員"]
    for text in soup.stripped_strings:
        if any(kw in text for kw in employee_keywords):
            return text
    return None




def extract_capital(soup):
    """extract capital from a given soup object"""

def extract_financial_status(soup):
    pass

def find_contact_form(soup, url):
    """find contact form from a given soup object"""
