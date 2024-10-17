# subweb

**subweb** is a Python package designed for finding subdomains of a given domain. It allows you to load subdomains from a file and check if they exist for a specific domain.

## Features

- Load subdomains from a text file.
- Check if subdomains exist for a given domain.
- Print only valid subdomains or handle both valid and invalid ones.
- Easy to use and install.

## Installation

```bash
pip install subweb
```

This will install the package along with the required dependencies.

## Usage

You can use `subweb` in your Python scripts after installation.

### Example 1: Print valid or wrong subdomains

This example checks subdomains for a domain and prints whether they are valid or wrong:

```python
import subweb

# Load subdomains from a file
subdomains = subweb.load_subdomains('subdomains.txt')

# Find subdomains for the given domain
scanning_result = subweb.find_subdomains('example.com', subdomains)

# Loop through results and print valid or wrong subdomain URLs
for subdomain_url, result in scanning_result.items():
    if result == 'valid':
        print(f"found_subdomain: {subdomain_url}")
    else:
        print(f"wrong subdomain: {subdomain_url}")
```

### Example 2: Print only valid subdomains

This example checks subdomains for a domain and prints only the valid ones:

```python
import subweb

# Load subdomains from a file
subdomains = subweb.load_subdomains('subdomains.txt')

# Find subdomains for the given domain
scanning_result = subweb.find_subdomains('example.com', subdomains)

# Loop through results and print only valid subdomain URLs
for subdomain_url, result in scanning_result.items():
    if result == 'valid':
        print(f"found_subdomains: {subdomain_url}")
```

### Example 3: Custom subdomain list in the code

If you prefer, you can also define the subdomains directly in your script instead of loading them from a file:

```python
import subweb

# Define subdomains directly
subdomains = ['www', 'mail', 'dev', 'help']

# Find subdomains for the given domain
scanning_result = subweb.find_subdomains('example.com', subdomains)

# Print the results
for subdomain_url, result in scanning_result.items():
    if result == 'valid':
        print(f"found_subdomains: {subdomain_url}")
    else:
        print(f"wrong subdomain: {subdomain_url}")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Made with ❤️ by [Fidal](https://github.com/mr-fidal) and [ByteBreach](https://github.com/ByteBreach).
