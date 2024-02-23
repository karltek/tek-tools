import requests
import json
from nicegui import ui
import os 
from dotenv import load_dotenv, dotenv_values


# API Keys import from .env
load_dotenv()
VT_KEY = os.getenv("VT_KEY")
ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY")
print(VT_KEY, ABUSEIPDB_KEY)


def ip_validate(input_data):
    from ipaddress import ip_address
    try:
        if ip_address(input_data):
            return True

    except Exception as e:
        return False

def hash_validation(hash: str) -> bool:
    """
    Returns True if characters in not_valid_chars list is not found in the hash.

    not_valid_chars = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    """
    not_valid_chars = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    return [x for x in not_valid_chars if x in hash.lower()] == []

def vt_check(ip: str = None, hash: str = None, domain: str = None):
    """Checks an IPv4 address or a Hash in Virus Total"""
    if ip is not None or hash is not None or domain is not None:
        if hash is None and domain is None:
            """IP check"""
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
            headers = {"accept": "application/json", "x-apikey": VT_KEY}
            response = requests.get(url, headers=headers)
            return response.json()
        
        elif ip is None and domain is None:
            """Hash check"""
            url = f"https://www.virustotal.com/api/v3/files/{hash}"
            headers = {"accept": "application/json", "x-apikey": VT_KEY}
            response = requests.get(url, headers=headers)
            return response.json()
        
        elif ip is None and hash is None:
            """Domain check"""
            url = f"https://www.virustotal.com/api/v3/domains/{domain}"
            headers = {"accept": "application/json", "x-apikey": VT_KEY}
            response = requests.get(url, headers=headers)
            return response.json()

def abuseipdb(ip):
    """
    Checks an IPv4 or IPv6 address in AbuseIPDB
    """
    url = 'https://api.abuseipdb.com/api/v2/check'
    querystring = {'ipAddress': ip,'maxAgeInDays': '90'}
    headers = { 'Accept': 'application/json','Key': ABUSEIPDB_KEY}
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    return response.json()

def Research() -> None:
    log.clear()
    # Checks if there is a value in text area and displays a warning if there is none
    if text_area.value == "":
        # log.push("Nothing to Research. Please enter data 1 per line. Check the placeholder value for example.")
        ui.notify("Nothing to Research. Please enter data 1 per line. Check the placeholder value for example.", position="top-right", type="warning")
    else:
        # Converts the entries into a Python list 
        converted_list = text_area.value.split("\n")
        converted_list_removed_empty = [x for x in converted_list if x]
        converted_list_final = list(dict.fromkeys(converted_list_removed_empty))
    
        # ui.notify("Validating your input.", position="top-right", type="info")
        # Results.set_text("Validating your input.")

        validated_list = []
        not_valid_ip = []

        for i in converted_list_final:
            # Checks if input is an IP
            if ip_validate(i):
                validated_list.append(i)
            else:
                not_valid_ip.append(i)
        
        if len(not_valid_ip) > 0:
            ui.notify(f"The following is/are not valid IP addresses.\n{not_valid_ip}", multi_line=True, type='negative', position="top-right")


        # Virustotal Lookup
        for i in validated_list:
            vt = vt_check(ip=i)
            vt_results = vt['data']['attributes']['last_analysis_stats']
            malicious = vt_results['malicious']
            suspicious = vt_results['suspicious']
            undetected = vt_results['undetected']
            harmless = vt_results['harmless']
            last_analysis_date = vt['data']['attributes']['last_analysis_date']
            whois = vt['data']['attributes']['whois']

        Results.set_text(f"According to Virustotal, the IP address: {i} has the following score \n \
                                {json.dumps(vt_results, indent=6)}")
            


ui.label("Research IPs, Domains, Hashes")
with ui.row().classes("flex flex-nowrap w-full h-full"):
    text_area = ui.textarea("Enter your data here!", placeholder="1.1.1.1\n8.8.8.8\n").props('clearable').classes("w-2/3")
    # Results = ui.label("Waiting for yodsdsd s dsds dsdwdwdw d wdw d ddwdwdwd adsdsdks d sdskd slk ur sds ds we wdsd sdswewewe dswdsds sdsddwinput")
    log = ui.log(max_lines=100).classes('w-1/3 h-1/3')
    # log.push("Test")
    # log.clear()

research_btn = ui.button("Research", on_click=Research).props("push").classes("flex")

# spinner = ui.spinner(size='lg')
# spinner.set_visibility(visible=False)


with ui.tabs() as tabs:
    ui.tab("Raw")
    ui.tab("Table")

with ui.tab_panels(tabs, value='Raw').classes("flex flex-nowrap w-full h-full"):

    with ui.tab_panel("Raw"):
        Results = ui.label()

    with ui.tab_panel("Table"):
        HEADERS = [
            {'name': 'type', 'label': 'Type', 'field': 'type', 'align': 'left'},
            {'name': 'age', 'label': 'Age', 'field': 'age', 'align': 'left'},
            {'name': 'age', 'label': 'Age', 'field': 'age', 'align': 'left'}
        ]
        rows = [
            {'type': 'Alice', 'age': 18},
            {'name': 'Bob', 'age': 21},
            {'name': 'Carol'},
        ]
        ui.table(columns=HEADERS, rows=rows, row_key='name', ).classes("flex flex-nowrap w-full h-full")




        
ui.run(port=8888, uvicorn_reload_includes='*.py', title="ktek", tailwind=True)