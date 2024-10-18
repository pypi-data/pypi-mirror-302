# MyInfo

**MyInfo** is a Python library for retrieving and formatting WHOIS and IP geolocation information. It allows you to easily get domain-related data such as registrar, creation date, expiry date, and DNS information, as well as IP geolocation details like city, country, and organization.

## Features

- Fetch WHOIS information for a domain.
- Resolve a domain to its IP address.
- Retrieve geolocation information for an IP address.
- Clean and simple API for integration into any Python project.

## Installation

```bash
pip install myinfo
```

## Usage

You can use the package to retrieve both WHOIS and IP information for any domain.

### Example Usage

#### 1. WHOIS Information

To fetch and format WHOIS information for a domain : 

```python
import myinfo

# Get WHOIS information
domain = "google.com"
whois_info = myinfo.get_whois_info(domain)

# Check for any errors
if 'error' not in whois_info:
    # Format WHOIS information
    formatted_whois = myinfo.format_whois_info(whois_info)
    
    # Example of displaying some information
    print(f"Domain Name: {formatted_whois['domain_name']}")
    print(f"Registrar: {formatted_whois['registrar']}")
    print(f"Creation Date: {formatted_whois['creation_date']}")
    print(f"Registry Expiry Date: {formatted_whois['registry_expiry_date']}")
    print(f"Name Servers: {formatted_whois['name_servers']}")
else:
    print(whois_info['error'])
```

#### 2. IP Geolocation Information

To resolve a domain to its IP and retrieve geolocation information for that IP :

```python
import myinfo

# WHOIS Information
domain = "google.com"
whois_info = myinfo.get_whois_info(domain)
if 'error' not in whois_info:
    formatted_whois = myinfo.format_whois_info(whois_info)
    print(f"Domain Name: {formatted_whois['domain_name']}")
    print(f"Registry Expiry Date: {formatted_whois['registry_expiry_date']}")
else:
    print(whois_info['error'])

# IP Geolocation Information
ip_address = myinfo.resolve_domain_to_ip(domain)
if isinstance(ip_address, dict) and 'error' in ip_address:
    print(ip_address['error'])
else:
    ip_info = myinfo.get_ip_geolocation(ip_address)
    if 'error' not in ip_info:
        formatted_ip_info = myinfo.format_ip_info(ip_address, ip_info)
        print(f"IP Address: {formatted_ip_info['ip_address']}")
        print(f"City: {formatted_ip_info['city']}")
        print(f"Country: {formatted_ip_info['country']}")
        print(f"Organization: {formatted_ip_info['organization']}")
    else:
        print(ip_info['error'])

```

### Functions

#### `get_whois_info(domain)`
- Retrieves WHOIS information for the given domain.
- **Parameters:**
    - `domain` (str): The domain name to get WHOIS information for.
- **Returns:**
    - A dictionary containing the WHOIS information or an error message.

#### `format_whois_info(domain_info)`
- Formats WHOIS information into a readable dictionary.
- **Parameters:**
    - `domain_info` (dict): The raw WHOIS data retrieved from the `get_whois_info()` function.
- **Returns:**
    - A dictionary containing formatted WHOIS data.

#### `resolve_domain_to_ip(domain)`
- Resolves a domain to its corresponding IP address.
- **Parameters:**
    - `domain` (str): The domain name to resolve.
- **Returns:**
    - The IP address (str) or an error message (dict).

#### `get_ip_geolocation(ip_address)`
- Retrieves geolocation information for a given IP address.
- **Parameters:**
    - `ip_address` (str): The IP address to get geolocation info for.
- **Returns:**
    - A dictionary containing IP geolocation information or an error message.

#### `format_ip_info(ip_info)`
- Formats IP geolocation information into a readable dictionary.
- **Parameters:**
    - `ip_info` (dict): The raw geolocation data retrieved from the `get_ip_geolocation()` function.
- **Returns:**
    - A dictionary containing formatted IP geolocation data.

## Example Output

For the domain `google.com` :

```
Domain Name: google.com  
Registrar: MarkMonitor Inc.  
Creation Date: 1997-09-15T04:00:00Z  
Registry Expiry Date: 2028-09-14T04:00:00Z  
Name Servers: ['NS1.GOOGLE.COM', 'NS2.GOOGLE.COM', 'NS3.GOOGLE.COM', 'NS4.GOOGLE.COM']

IP Address: 172.217.12.14  
City: Mountain View  
Country: US  
Organization: GOOGLE
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
