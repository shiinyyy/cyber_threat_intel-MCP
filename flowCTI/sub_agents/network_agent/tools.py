import requests
import os
import json
import time
from typing import Dict, Any
from dotenv import load_dotenv
import traceback

load_dotenv()

# IP ADDRESSES 
def getIP(ip: str) -> str: 
    VT_API=os.getenv("VT_API_KEY")
    url=f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"

    headers = {
        "accept": "application/json",
        "x-apikey": VT_API
    }

    try:
        print("Making request to:", url)
        print("Using API key:", VT_API[:6] + "..." if VT_API else "None")
        response = requests.get(url, headers=headers)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        return response.json()
    except Exception as e:
        print("Exception during request:", e)
        traceback.print_exc()
        return None

# Parsing retrieved data
def ip_parsing(data: Dict[str, Any]) -> None:
    ip_data = data.get('data', {})
    attributes = ip_data.get('attributes', {})
    stats = attributes.get('last_analysis_stats', {})
    tags = attributes.get('tags', [])
    reputation = attributes.get('reputation', 'N/A')
    whois = attributes.get('whois', '').split('\n')[0:5] # first 5 lines
    
    print(f"IP Address: {ip_data.get('id', 'N/A')}")
    print(f"Reputation: {reputation}")
    print(f"Tags: {', '.join(tags) if tags else 'None'}")
    print(f"Last Analysis Stats:")
    for k, v in stats.items():
        print(f"  {k.capitalize()}: {v}")
    print(f"Whois:")
    for line in whois:
        print(f" {line}")

    # Display malicious flagged
    results = attributes.get('last_analysis_results', {})
    malicious_engines = [k for k, v in results.items() if v.get('category') == 'malicious']
    if malicious_engines:
        print("Malicious engines:")
        for engine in malicious_engines:
            print(f" {engine}")
    else:
        print(f"No malicious flagged for this IP")
#___________________________________________________________________________________________
# URL SCANNING AND REPORT
def postURL(target_url: str) -> str:
    VT_API=os.getenv("VT_API_KEY")
    endpoint="https://www.virustotal.com/api/v3/urls"
    
    headers= {
        "accept": "application/json",
        "x-apikey": VT_API,
    }
    data = {"url": target_url}
    response = requests.post(endpoint, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        analysis_id = result.get('data', {}).get('id')
        print(f"URL submitted. Analysis ID: {analysis_id}")
        return analysis_id
    else:
        print(f"Error submitting URL: {response.status_code} - {response.text}")
        return None

# Get report from the urls
def getURL(analysis_id: str) -> Dict[str, Any]:
    VT_API=os.getenv("VT_API_KEY")
    endpoint=f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    
    headers= {
        "accept": "application/json",
        "x-apikey": VT_API,
    }
    
    response = requests.get(endpoint, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
        return data
    else:
        print(f"Error retrieving report: {response.status_code} - {response.text}")
        return None

# Parsing report
def url_parsing(data: Dict[str, Any]) -> None:
    attributes = data.get('data', {}).get('attributes', {})
    stats = attributes.get('stats', {})
    results = attributes.get('results', {})
                             
    print("\nURL Analysis:")
    print("Stats:")
    for category, count in stats.items():
        print(f"  {category.capitalize()}: {count}")
        
    print("\nDetections:")
    malicious_engines = [
        engine for engine, result in results.items()
        if result.get('category') == 'malicious'
    ]
    
    if malicious_engines:
        print("Malicious engines detected:")
        for engine in malicious_engines:
            print(f"  - {engine}")
    else:
        print("No malicious engines detected.")
        
# Binding as tool
def scanURL(url: str) -> dict:
    analysis_id = postURL(url)
    if not analysis_id:
        return {"error": "Failed to submit url."}
    time.sleep(15)
    report = getURL(analysis_id)
    if not report:
        return {"error": "Failed to retrieve data for report."}
    return report