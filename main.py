# ---------------------------------------------------------
# Developed and maintained by labounq.
# GitHub profile: https://github.com/labounq
# For any inquiries or support, reach out on Telegram: https://t.me/Aznannnnls1903l
# ---------------------------------------------------------
import json
import time
import requests
import urllib.parse
from urllib.parse import urlencode
from collections import OrderedDict
from api import register_device_api, generate_guards, encrypt_payload, sign_request
from utils import generate_ids, xor_email, get_base_params, get_base_headers, inject_python_headers, generate_password

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def run():
    print("[*] Starting Standalone Registration Flow...")
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("RAPIDAPI_KEY"):
        print("\n[-] Error: No RapidAPI key found.")
        print("[-] Please create a '.env' file in this directory and add your key: RAPIDAPI_KEY=your_key_here")
        print("[-] You can get a free API key at: https://rapidapi.com/labouakileed122/api/tiktok-signer-working")
        print("[-] Press Enter to exit...")
        input()
        return

    config = load_config()
    ids = generate_ids()
    session = requests.Session()
    
    email = None

    # ---------------------------------------------------------
    # 1. Device Register
    # ---------------------------------------------------------
    print("\n--- 1. Device Register ---")
    now_ms = int(time.time() * 1000)
    base_params = get_base_params(config, ids)
    
    # In original device_register, params has req_id
    dr_params = base_params.copy()
    dr_params["req_id"] = ids["req_id"]
    dr_params["tt_data"] = "a"
    
    payload_data = {
        "header": {
            "os": "Android", 
            "os_version": config["device"]["os_version"], 
            "os_api": config["device"]["os_api"],
            "device_model": config["device"]["device_model"], 
            "device_brand": config["device"]["device_brand"],
            "device_manufacturer": config["device"]["device_manufacturer"], 
            "cpu_abi": "arm64-v8a",
            "density_dpi": config["device"]["density_dpi"], 
            "display_density": config["device"]["display_density"],
            "resolution": config["device"]["resolution"], 
            "display_density_v2": config["device"]["display_density"],
            "resolution_v2": config["device"]["resolution"], 
            "access": "wifi",
            "rom": config["device"]["rom"], 
            "rom_version": config["device"]["rom_version"],
            "language": "en", 
            "timezone": config["device"]["timezone_offset"] // 3600,
            "tz_name": config["device"]["timezone_name"], 
            "tz_offset": config["device"]["timezone_offset"],
            "sim_region": config["device"]["sim_region"], 
            "carrier": config["device"]["carrier"],
            "mcc_mnc": config["device"]["mcc_mnc"], 
            "clientudid": ids["clientudid"],
            "openudid": ids["openudid"], 
            "req_id": ids["req_id"],
            "cdid": ids["cdid"], 
            "google_aid": ids["google_aid"],
            "apk_first_install_time": ids["apk_first_install_time"],
            "custom": {
                "is_flip": 0, "is_foldable": 0, "dark_mode_setting_value":1,
                "filter_warn": 0, "priority_region": config["device"]["sim_region"].upper(),
                "user_period": 0, "is_kids_mode": 0, 
                "web_ua": f"Dalvik/2.1.0 (Linux; U; Android {config['device']['os_version']}; {config['device']['device_model']} Build/{config['device']['rom']})", 
                "user_mode": -1,
                "ram_size": config["device"]["ram_size"],
                "screen_height_dp": int(config["device"]["screen_height_dp"]),
                "screen_width_dp": int(config["device"]["screen_width_dp"])
            },
            "channel": config["app"]["channel"], "not_request_sender": 1, "aid": config["app"]["aid"],
            "release_build": "d711eec_20260716", "ab_version": config["app"]["version_name"], "gaid_limited": 0,
            "package": "com.zhiliaoapp.musically", "app_version": config["app"]["version_name"],
            "app_version_minor": "", "version_code": config["app"]["version_code"],
            "update_version_code": config["app"]["update_version_code"], "manifest_version_code": config["app"]["manifest_version_code"],
            "app_name": config["app"]["app_name"], "tweaked_channel": config["app"]["channel"],
            "display_name": "TikTok", "sig_hash": "194326e82c84a639a52e5c023116f12a",
            "device_platform": "android", "git_hash": "b53ca20",
            "sdk_version_code": 205140590, "sdk_target_version": 30,
            "sdk_version": "2.5.14.5", "guest_mode": 0, "sdk_flavor": "i18nInner", "is_system_app": 0
        },
        "magic_tag": "ss_app_log",
        "_gen_time": now_ms - 4000
    }
    
    payload_str_clear = json.dumps(payload_data, separators=(',', ':'))
    
    print("[*] Encrypting device_register payload via RapidAPI...")
    encrypted_bytes = encrypt_payload(payload_str_clear)
    if not encrypted_bytes:
        print("[-] Encryption failed. Exiting.")
        return
        
    dr_url_base = "https://log-boot.tiktokv.com/service/2/device_register/"
    dr_url = f"{dr_url_base}?{urlencode(dr_params)}"
    
    headers_dr = get_base_headers(config)
    headers_dr["x-ss-req-ticket"] = str(now_ms)
    headers_dr["x-tt-dm-status"] = "login=0;ct=0;rt=7"
    headers_dr["content-type"] = "application/octet-stream;tt-data=a"
    headers_dr["log-encode-type"] = "gzip"
    
    # Inject python headers (stub, trace-id, req-ticket) for RapidAPI signer
    # Pass the CLEAR payload to sign!
    headers_dr = inject_python_headers(headers_dr, payload_str_clear, "POST", "0", config["app"]["aid"])
    
    sigs = sign_request(dr_url, headers_dr, session.cookies.get_dict(), config["device"]["device_model"], config["device"]["os_version"], config["app"]["version_name"])
    if sigs and sigs.get("data"):
        for k, v in sigs["data"].items():
            headers_dr[k.lower()] = v
            
    # Remove x-tt-ttnet-origin-host explicitly for the first request if added
    headers_dr.pop("x-tt-ttnet-origin-host", None)
    
    resp_dr = session.post(dr_url, data=encrypted_bytes, headers=headers_dr)
    print(f" > Device Register Status: {resp_dr.status_code}")
    
    try:
        dr_data = resp_dr.json()
        ids["device_id"] = str(dr_data.get("device_id", ""))
        ids["install_id"] = str(dr_data.get("install_id", ""))
        print(f" > Got Device ID: {ids['device_id']}")
        print(f" > Got Install ID: {ids['install_id']}")
        
        # Capture cookies
        if 'set-cookie' in resp_dr.headers or 'Set-Cookie' in resp_dr.headers:
            raw_cookies = resp_dr.raw.headers.getlist('Set-Cookie') or resp_dr.raw.headers.getlist('set-cookie')
            for cookie_str in raw_cookies:
                cookie_main = cookie_str.split(';')[0]
                if '=' in cookie_main:
                    c_name, c_value = cookie_main.split('=', 1)
                    session.cookies.set(c_name.strip(), c_value.strip())
                    
    except Exception as e:
        print(f"[-] Failed to parse device_register response: {e}")
        return
        


    # ---------------------------------------------------------
    # 2. Age Verification
    # ---------------------------------------------------------
    print("\n--- 2. Age Verification ---")
    age_params = get_base_params(config, ids)
    import random
    birth_year = random.randint(1990, 2007)
    birth_month = random.randint(1, 12)
    birth_day = random.randint(1, 28)
    birthday_str = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
    
    age_params["birthday"] = birthday_str
    age_params["update_birthdate_type"] = "1"
    age_params["session_registered"] = "1"
    age_params["is_guest"] = "false"
    age_params["birthday_confidence"] = "0"
    age_params["iid"] = ids["install_id"]
    age_params["device_id"] = ids["device_id"]
    age_params["reg_store_region"] = config["device"]["sim_region"].upper()
    age_params["user_selected_region"] = "0"
    age_params["sys_region"] = config["device"]["sim_region"].upper()
    age_params["op_region"] = config["device"]["sim_region"].upper()
    age_params["region"] = config["device"]["sim_region"].upper()
    
    age_url_base = "https://aggr32-normal.tiktokv.eu/aweme/v3/verification/age/"
    age_url = f"{age_url_base}?{urlencode(age_params)}"
    
    age_payload = ""
    
    age_headers = get_base_headers(config)
    age_headers["x-tt-dm-status"] = "login=0;ct=0;rt=7"
    age_headers["x-ss-req-ticket"] = str(int(time.time() * 1000))
    age_headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    age_headers["x-tt-store-region"] = config["device"]["sim_region"].lower()
    age_headers["x-tt-store-region-src"] = "did"
    age_headers["x-tt-request-tag"] = "s=-1;p=0"
    age_headers["rpc-persist-pyxis-policy-v-tnc"] = "1"
    age_headers["x-tt-ttnet-origin-host"] = "api32-normal-no1a.tiktokv.eu"
    
    age_headers = inject_python_headers(age_headers, age_payload, "POST", ids["device_id"], config["app"]["aid"])
    
    sigs = sign_request(age_url, age_headers, session.cookies.get_dict(), config["device"]["device_model"], config["device"]["os_version"], config["app"]["version_name"])
    if sigs and sigs.get("data"):
        for k, v in sigs["data"].items():
            age_headers[k.lower()] = v
            
    resp_age = session.post(age_url, data=age_payload, headers=age_headers)
    print(f" > Age Verification Status: {resp_age.status_code}")

    print("\n[*] Registering device on RapidAPI for future guards...")
    register_device_api(ids, config, session.cookies.get_dict())
    
    # Ensure tt_ticket_guard_has_set_public_key=1
    session.cookies.set("tt_ticket_guard_has_set_public_key", "1")
    session.cookies.set("install_id", ids["install_id"])

    email = input("\nEnter email to register: ").strip()
    if not email:
        return


    # ---------------------------------------------------------
    # 5. Send Code
    # ---------------------------------------------------------
    print("\n--- 5. Send Code ---")
    send_params = get_base_params(config, ids)
    send_params["iid"] = ids["install_id"]
    send_params["device_id"] = ids["device_id"]
    send_params["current_region"] = config["device"]["sim_region"].upper()
    send_params["residence"] = config["device"]["sim_region"].upper()
    send_params["support_webview"] = "1"
    send_params["reg_store_region"] = config["device"]["sim_region"].upper()
    send_params["sys_region"] = "US"
    
    send_url_base = f"https://api16-normal-no1a.tiktokv.eu/passport/email/send_code/"
    send_url = f"{send_url_base}?{urlencode(send_params)}"
    
    send_payload = urlencode({
        "account_sdk_source": "app",
        "rule_strategies": "2",
        "mix_mode": "1",
        "multi_login": "1",
        "type": "3732", 
        "email": xor_email(email),
        "email_theme": "2"
    })
    
    guards = generate_guards(send_url, ids["device_id"])
    pub_key = ""
    client_data = ""
    if guards and guards.get("status") == "success" and "data" in guards:
        pub_key = guards["data"].get("tt-ticket-guard-public-key", "")
        client_data = guards["data"].get("tt-device-guard-client-data", "")
        
    send_headers = get_base_headers(config)
    send_headers["x-tt-pba-enable"] = "1"
    send_headers["tt-ticket-guard-version"] = "3"
    send_headers["tt-ticket-guard-iteration-version"] = "0"
    send_headers["passport-sdk-settings"] = "x-tt-token"
    send_headers["passport-sdk-sign"] = "x-tt-token"
    send_headers["x-tt-bypass-dp"] = "1"
    send_headers["x-tt-dm-status"] = "login=0;ct=1;rt=8"
    send_headers["oec-cs-si-a"] = "2"
    send_headers["oec-cs-sdk-version"] = "v10.02.11-ov-android"
    send_headers["oec-vc-sdk-version"] = "3.2.3.i18n"
    send_headers["tt-device-guard-iteration-version"] = "1"
    send_headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    send_headers["x-tt-request-tag"] = "s=-1;p=0"
    send_headers["tt-ticket-guard-public-key"] = pub_key
    send_headers["tt-device-guard-client-data"] = client_data
    send_headers["x-tt-ttnet-origin-host"] = "api19-normal-no1a.tiktokv.eu"
    
    send_headers = inject_python_headers(send_headers, send_payload, "POST", ids["device_id"], config["app"]["aid"])
    
    sigs = sign_request(send_url, send_headers, session.cookies.get_dict(), config["device"]["device_model"], config["device"]["os_version"], config["app"]["version_name"])
    if sigs and sigs.get("data"):
        for k, v in sigs["data"].items():
            send_headers[k.lower()] = v
            
    resp_send = session.post(send_url, data=send_payload, headers=send_headers)
    print(f" > Send Code Status: {resp_send.status_code}")
    print(f" > Send Code Response: {resp_send.text[:200]}")
    
    tg_server_data = resp_send.headers.get("tt-ticket-guard-server-data")
    if not tg_server_data:
        try:
            tg_server_data = resp_send.json().get("data", {}).get("tt-ticket-guard-server-data", "")
        except: pass

    # ---------------------------------------------------------
    # 6. Verify Registration Code
    # ---------------------------------------------------------
    code = input("\nEnter the verification code received on email: ").strip()
    if not code:
        return

    print("\n--- 6. Register Verify Login ---")
    ver_params = get_base_params(config, ids)
    ver_params["iid"] = ids["install_id"]
    ver_params["device_id"] = ids["device_id"]
    ver_params["current_region"] = config["device"]["sim_region"].upper()
    ver_params["residence"] = config["device"]["sim_region"].upper()
    ver_params["support_webview"] = "1"
    ver_params["reg_store_region"] = config["device"]["sim_region"].upper()
    ver_params["sys_region"] = "US"
    ver_params["passport-sdk-version"] = "1"
    
    ver_url_base = f"https://api16-normal-no1a.tiktokv.eu/passport/email/register_verify_login/"
    ver_url = f"{ver_url_base}?{urlencode(ver_params)}"
    
    ver_payload = urlencode({
        "birthday": birthday_str,
        "fixed_mix_mode": "1",
        "code": xor_email(code),
        "account_sdk_source": "app",
        "mix_mode": "1",
        "multi_login": "1",
        "type": "3732",
        "email": xor_email(email)
    })
    
    guards_tk = generate_guards(ver_url, ids["device_id"], tg_server_data)
    pub_key = ""
    client_data = ""
    ticket_data = ""
    if guards_tk and guards_tk.get("status") == "success" and "data" in guards_tk:
        pub_key = guards_tk["data"].get("tt-ticket-guard-public-key", "")
        client_data = guards_tk["data"].get("tt-device-guard-client-data", "")
        ticket_data = guards_tk["data"].get("tt-ticket-guard-client-data", "")
        
    ver_headers = get_base_headers(config)
    ver_headers["x-tt-pba-enable"] = "1"
    ver_headers["tt-ticket-guard-version"] = "3"
    ver_headers["tt-ticket-guard-iteration-version"] = "0"
    ver_headers["passport-sdk-settings"] = "x-tt-token"
    ver_headers["passport-sdk-sign"] = "x-tt-token"
    ver_headers["x-tt-bypass-dp"] = "1"
    ver_headers["oec-cs-si-a"] = "2"
    ver_headers["oec-cs-sdk-version"] = "v10.02.11-ov-android"
    ver_headers["oec-vc-sdk-version"] = "3.2.3.i18n"
    ver_headers["tt-device-guard-iteration-version"] = "1"
    ver_headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    ver_headers["x-tt-request-tag"] = "s=-1;p=0"
    ver_headers["x-tt-dm-status"] = "login=0;ct=1;rt=8"
    ver_headers["x-tt-ttnet-origin-host"] = "api19-normal-no1a.tiktokv.eu"
    
    if pub_key: ver_headers["tt-ticket-guard-public-key"] = pub_key
    if client_data: ver_headers["tt-device-guard-client-data"] = client_data
    if ticket_data: ver_headers["tt-ticket-guard-client-data"] = ticket_data
    
    ver_headers = inject_python_headers(ver_headers, ver_payload, "POST", ids["device_id"], config["app"]["aid"])
    
    sigs = sign_request(ver_url, ver_headers, session.cookies.get_dict(), config["device"]["device_model"], config["device"]["os_version"], config["app"]["version_name"])
    if sigs and sigs.get("data"):
        for k, v in sigs["data"].items():
            ver_headers[k.lower()] = v
            
    resp_ver = session.post(ver_url, data=ver_payload, headers=ver_headers)
    print(f" > Register Verify Status: {resp_ver.status_code}")
    print(f" > Final Response: {resp_ver.text[:1000]}")
    
    try:
        ver_json = resp_ver.json()
        username = ver_json.get("data", {}).get("name")
    except:
        ver_json = {}
        username = None

    if not username:
        print("\n[-] Account creation failed!")
        print("[-] This error occurs because either your VPN/proxy IP is flagged, or the email domain has been used too many times recently.")
        print("[-] Please switch your VPN/proxy or try a different email domain.")
        return
        
    print(f"\n[+] Account created successfully! Profile: https://tiktok.com/@{username}")
    
    # Extraction and Saving
    final_tg_server_data = resp_ver.headers.get("tt-ticket-guard-server-data", "")
    
    password = generate_password()
    
    account_data = {
        "email": email,
        "password": password,
        "birthday": birthday_str,
        "device_id": ids["device_id"],
        "install_id": ids["install_id"],
        "cdid": ids.get("cdid", ""),
        "clientudid": ids.get("clientudid", ""),
        "openudid": ids.get("openudid", ""),
        "google_aid": ids.get("google_aid", ""),
        "req_id": ids.get("req_id", ""),
        "apk_first_install_time": ids.get("apk_first_install_time", 0),
        "cookies": session.cookies.get_dict(),
        "final_tg_server_data": final_tg_server_data,
        "response_headers": dict(resp_ver.headers),
        "response": resp_ver.json() if resp_ver.status_code == 200 else resp_ver.text
    }
    
    import os
    os.makedirs("accounts", exist_ok=True)
    
    with open(os.path.join("accounts", f"{email}.json"), "w") as f:
        json.dump(account_data, f, indent=4)
        
    print(f"\n[+] Account & Device data saved to accounts/{email}.json")
    print(f"[+] Password generated: {password}")

if __name__ == "__main__":
    run()
