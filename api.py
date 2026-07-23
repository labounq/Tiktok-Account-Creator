# =========================================================
# This script was made by https://github.com/labounq
# Need help, custom scripts, or anything related to Tiktok? Contact me at https://t.me/Aznannnnls1903l
# =========================================================
import os
import json
import base64
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")

# Base headers for RapidAPI
RAPIDAPI_HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "tiktok-signer-working.p.rapidapi.com",
    "Content-Type": "application/json"
}



def sign_request(url, headers, cookies, device_model, os_version, tiktok_version):
    """
    Sends data to /sign to generate x-gorgon, x-argus, x-ladon, and x-khronos.
    """
    payload = {
        "url": url,
        "os_version": os_version,
        "device_model": device_model,
        "tiktok_version": tiktok_version,
        "headers": headers,
        "cookies": cookies
    }
    
    resp = requests.post(
        "https://tiktok-signer-working.p.rapidapi.com/sign", 
        json=payload, 
        headers=RAPIDAPI_HEADERS
    )
    
    if resp.status_code == 403 or resp.status_code == 429:
        print("\n[-] RapidAPI Error: You have reached your API limits or no valid key was provided.")
        print("[-] Please subscribe to a plan (it's free) to get your own API key here:")
        print("[-] https://rapidapi.com/labouakileed122/api/tiktok-signer-working\n")
        return None
        
    try:
        return resp.json()
    except Exception as e:
        print(f"[-] RapidAPI Sign Error: {resp.text}")
        return None

def register_device_api(ids, config, cookies, domain="tiktokv.eu", store_idc="no1a"):
    """
    Registers the device on RapidAPI so that guards can be generated later.
    """
    payload = {
        "device_id": str(ids.get("device_id", "")),
        "install_id": str(ids.get("install_id", "")),
        "model": config["device"]["device_model"],
        "device_manufacturer": config["device"]["device_manufacturer"],
        "rom": config["device"]["rom"],
        "ttreq": cookies.get("ttreq", ""),
        "odin_tt": cookies.get("odin_tt", ""),
        "store_country_sign": cookies.get("store-country-code", ""),
        "os_version": config["device"]["os_version"],
        "region": config["device"]["sim_region"].lower(),
        "app_version": config["app"]["version_name"],
        "language": "en",
        "timezone_name": config["device"]["timezone_name"],
        "timezone_offset": str(config["device"]["timezone_offset"]),
        "cdid": ids.get("cdid", ""),
        "google_aid": ids.get("google_aid", ""),
        "openudid": ids.get("openudid", ""),
        "store_idc": store_idc,
        "domain": domain,
        "dpi": str(config["device"]["density_dpi"]),
        "resolution": config["device"]["resolution"]
    }
    
    resp = requests.post(
        "https://tiktok-signer-working.p.rapidapi.com/register_device", 
        json=payload, 
        headers=RAPIDAPI_HEADERS
    )
    
    if resp.status_code == 403 or resp.status_code == 429:
        print("\n[-] RapidAPI Error: You have reached your API limits or no valid key was provided.")
        print("[-] Please subscribe to a plan (it's free) to get your own API key here:")
        print("[-] https://rapidapi.com/labouakileed122/api/tiktok-signer-working/pricing\n")
        return None
        
    try:
        return resp.json()
    except Exception as e:
        print(f"[-] RapidAPI Register Device Error: {resp.text}")
        return None

def generate_guards(url, device_id, tt_ticket_guard_server_data=""):
    """
    Generates tt-device-guard-client-data and tt-ticket-guard-client-data.
    Requires the device to have been registered via register_device_api first.
    """
    payload = {
        "url": url,
        "device_id": device_id
    }
    if tt_ticket_guard_server_data:
        payload["tt_ticket_guard_server_data"] = tt_ticket_guard_server_data
        
    resp = requests.post(
        "https://tiktok-signer-working.p.rapidapi.com/generate_guards", 
        json=payload, 
        headers=RAPIDAPI_HEADERS
    )
    
    if resp.status_code == 403 or resp.status_code == 429:
        print("\n[-] RapidAPI Error: You have reached your API limits or no valid key was provided.")
        print("[-] Please subscribe to a plan (it's free) to get your own API key here:")
        print("[-] https://rapidapi.com/labouakileed122/api/tiktok-signer-working\n")
        return None
        
    try:
        return resp.json()
    except Exception as e:
        print(f"[-] RapidAPI Generate Guards Error: {resp.text}")
        return None

def encrypt_payload(payload_str):
    """
    Encrypts the payload via RapidAPI /encrypt endpoint and returns the base64 decoded raw bytes.
    """
    
    resp = requests.post(
        "https://tiktok-signer-working.p.rapidapi.com/encrypt", 
        data=payload_str, 
        headers=RAPIDAPI_HEADERS
    )
    
    if resp.status_code == 403 or resp.status_code == 429:
        print("\n[-] RapidAPI Error: You have reached your API limits or no valid key was provided.")
        print("[-] Please subscribe to a plan (it's free) to get your own API key here:")
        print("[-] https://rapidapi.com/labouakileed122/api/tiktok-signer-working\n")
        return None
        
    try:
        data = resp.json()
        if data.get("status") == "success" and "encrypted_data_b64" in data:
            return base64.b64decode(data["encrypted_data_b64"])
        else:
            print(f"[-] RapidAPI Encrypt Error: {data}")
            return None
    except Exception as e:
        print(f"[-] RapidAPI Encrypt Exception: {resp.text}")
        return None
