import requests

def load_subdomains(file_path):
    try:
        with open(file_path, 'r') as file:
            subdomains = [line.strip() for line in file]
        return subdomains
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")

def find_subdomains(domain, subdomain_list):
    found_subdomains = {}
    
    for subdomain in subdomain_list:
        url = f"https://{subdomain}.{domain}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                found_subdomains[url] = 'valid'
            else:
                found_subdomains[url] = 'invalid'
        
        except requests.ConnectionError:
            found_subdomains[url] = 'invalid'
    
    return found_subdomains
