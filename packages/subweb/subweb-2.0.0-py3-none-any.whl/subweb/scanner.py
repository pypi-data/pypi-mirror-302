import requests
from requests.exceptions import ConnectionError, Timeout

def get_website_info(url):
    info = {}
    try:
        response = requests.get(url, timeout=5)
        info['url'] = url
        info['status_code'] = response.status_code
        info['title'] = extract_title(response.text)
        info['server'] = response.headers.get('Server', 'Unknown')
        info['ip_address'] = response.raw._connection.sock.getpeername()[0]
    except ConnectionError:
        info['error'] = 'Connection Error'
    except Timeout:
        info['error'] = 'Timeout'
    
    return info

def extract_title(html):
    start = html.find('<title>')
    end = html.find('</title>', start)
    if start != -1 and end != -1:
        return html[start + 7:end].strip()
    return 'No Title'

def subdomain_scan(domain, subdomains):
    found_info = []
    for sub in subdomains:
        subdomain = f"http://{sub}.{domain}"
        info = get_website_info(subdomain)
        if 'status_code' in info and info['status_code'] == 200:
            found_info.append(info)
    return found_info
