import socket
from ipwhois import IPWhois

def resolve_domain_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return {"error": f"Could not resolve {domain} to an IP address."}

def get_ip_geolocation(ip_address):
    try:
        obj = IPWhois(ip_address)
        ip_info = obj.lookup_rdap()
        return ip_info
    except Exception as e:
        return {"error": f"Error fetching IP information: {e}"}

def format_ip_info(ip_address, ip_info):
    return {
        "ip_address": ip_address,  # Include the actual IP address
        "city": ip_info.get('network', {}).get('city', 'N/A'),  # Correct city extraction
        "country": ip_info.get('asn_country_code', 'N/A'),
        "range": f"{ip_info.get('network', {}).get('start_address', 'N/A')} - {ip_info.get('network', {}).get('end_address', 'N/A')}",
        "organization": ip_info.get('asn_description', 'N/A')  # Use description for better clarity
    }
