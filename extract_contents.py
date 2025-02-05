import re
import requests

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
