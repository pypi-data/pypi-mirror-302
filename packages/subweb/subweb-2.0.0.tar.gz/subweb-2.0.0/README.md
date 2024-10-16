# Subweb Package

The Subweb package is a Python library designed for scanning and retrieving information about subdomains for a given domain. It provides functionalities to find subdomains, retrieve their status codes, titles, and more.

## Installation

To install the Subweb package, use pip:

```bash
pip install subweb
```

## Usage

### Scanning Subdomains

You can scan subdomains by creating a script that uses the `subdomain_scan` function from the `subweb` package. Below are several examples of how to use this package.

#### Example: Find Subdomains

```python
from subweb import subdomain_scan

def display_found_subdomains(domain, subdomains):
    found_info = subdomain_scan(domain, subdomains)
    return [info['url'] for info in found_info]

if __name__ == "__main__":
    target_domain = "example.com"  # Replace with your target domain
    subdomains = ["www", "api", "blog", "test"]  # Replace with your subdomain list

    found_subdomains = display_found_subdomains(target_domain, subdomains)
    for sub in found_subdomains:
        print(f"Found subdomain: {sub}")
```

#### Example: Subdomains with Status Codes

```python
from subweb import subdomain_scan

def display_status_codes_with_found(domain, subdomains):
    found_info = subdomain_scan(domain, subdomains)
    return [(info['url'], info['status_code']) for info in found_info]

if __name__ == "__main__":
    target_domain = "example.com"  # Replace with your target domain
    subdomains = ["www", "api", "blog", "test"]  # Replace with your subdomain list

    status_codes = display_status_codes_with_found(target_domain, subdomains)
    for url, code in status_codes:
        print(f"Found subdomain: {url} with Status Code: {code}")
```

#### Example: Subdomains with Titles

```python
from subweb import subdomain_scan

def display_titles_with_found(domain, subdomains):
    found_info = subdomain_scan(domain, subdomains)
    return [(info['url'], info['title']) for info in found_info]

if __name__ == "__main__":
    target_domain = "example.com"  # Replace with your target domain
    subdomains = ["www", "api", "blog", "test"]  # Replace with your subdomain list

    titles = display_titles_with_found(target_domain, subdomains)
    for url, title in titles:
        print(f"Found subdomain: {url} with Title: {title}")
```

#### Example: Full Info of Subdomains

```python
from subweb import subdomain_scan

def display_full_info_with_found(domain, subdomains):
    found_info = subdomain_scan(domain, subdomains)
    return found_info

if __name__ == "__main__":
    target_domain = "example.com"  # Replace with your target domain
    subdomains = ["www", "api", "blog", "test"]  # Replace with your subdomain list

    full_info = display_full_info_with_found(target_domain, subdomains)
    for info in full_info:
        print(f"Found subdomain: {info['url']}")
        print(f"Status Code: {info.get('status_code', 'N/A')}")
        print(f"Title: {info.get('title', 'N/A')}")
        print(f"Server: {info.get('server', 'N/A')}")
        print(f"IP Address: {info.get('ip_address', 'N/A')}")
        print("-" * 40)
```

### Reading Subdomains from a File

You can also read subdomains from a file. Here’s how to implement it:

```python
def read_subdomains_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Example usage
if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., example.com): ")
    subdomain_file = input("Enter the path to the subdomain list file: ")

    subdomains = read_subdomains_from_file(subdomain_file)
    # Call your desired function with the loaded subdomains
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Acknowledgements

- [Subweb](https://github.com/ByteBreach/subweb) for the subdomain scanning functionality.
