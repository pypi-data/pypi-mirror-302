import requests
import re
from urllib.parse import quote

def load_payloads_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []

def test_xss_payloads(target, payloads, method='GET'):
    results = []
    for index, payload in enumerate(payloads, 1):
        encoded_payload = quote(payload)
        url = f"{target}?input={encoded_payload}"
        headers = {'User-Agent': 'Mozilla/5.0 (XSS Testing Tool)'}
        
        try:
            if method == 'POST':
                response = requests.post(target, data={'input': payload}, headers=headers, timeout=5)
            else:
                response = requests.get(url, headers=headers, timeout=5)

            vulnerable = any(keyword in response.text.lower() for keyword in ['alert', 'cookie'])
            results.append((payload, url, vulnerable, response.status_code))

        except requests.RequestException as e:
            results.append((payload, url, False, str(e)))

    return results

def is_valid_url(url):
    # Basic URL validation
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  
        r'localhost|'  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  
        r'(?::\d+)?'  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

def format_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url
