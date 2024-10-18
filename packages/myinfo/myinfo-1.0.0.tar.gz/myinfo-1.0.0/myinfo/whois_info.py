import whois
from datetime import datetime

def get_whois_info(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        return {"error": f"Error fetching WHOIS information : {e}"}

def format_whois_info(domain_info):
    def format_date(date):
        if isinstance(date, list):
            date = date[0]
        return date.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(date, datetime) else str(date)

    return {
        "domain_name": domain_info.domain_name,
        "registry_domain_id": domain_info.get('domain_id', 'N/A'),
        "whois_server": domain_info.get('whois_server', 'N/A'),
        "registrar_url": domain_info.get('registrar_url', 'N/A'),
        "updated_date": format_date(domain_info.updated_date),
        "creation_date": format_date(domain_info.creation_date),
        "registry_expiry_date": format_date(domain_info.expiration_date),
        "registrar": domain_info.get('registrar', 'N/A'),
        "domain_status": domain_info.status if domain_info.status else 'N/A',
        "name_servers": domain_info.name_servers if domain_info.name_servers else 'N/A',
        "dnssec": domain_info.get('dnssec', 'N/A')
    }
