# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Utilities made by labounq (Find me: https://github.com/labounq)
# For questions, collabs, or business: https://t.me/Aznannnnls1903l
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import uuid
import random
import string
import secrets
import time
import hashlib
from urllib.parse import urlencode

def generate_password():
    length = random.randint(12, 18)
    allowed_symbols = "!$%"
    
    mandatory_digits = [secrets.choice(string.digits) for _ in range(2)]
    mandatory_symbols = [secrets.choice(allowed_symbols) for _ in range(2)]
    
    all_characters = string.ascii_letters + string.digits + allowed_symbols
    
    remaining_length = length - len(mandatory_digits) - len(mandatory_symbols)
    remaining_chars = [secrets.choice(all_characters) for _ in range(remaining_length)]
    
    password_list = mandatory_digits + mandatory_symbols + remaining_chars
    secrets.SystemRandom().shuffle(password_list)
    
    return ''.join(password_list)

def generate_ids():
    """Generates random tracking IDs per session."""
    now_ms = int(time.time() * 1000)
    install_window_start = now_ms - (2 * 60 * 60 * 1000)
    install_window_end = now_ms - (5 * 60 * 1000)
    
    return {
        "cdid": str(uuid.uuid4()),
        "google_aid": str(uuid.uuid4()),
        "openudid": ''.join(random.choices('0123456789abcdef', k=16)),
        "clientudid": str(uuid.uuid4()),
        "req_id": str(uuid.uuid4()),
        "apk_first_install_time": random.randint(install_window_start, install_window_end)
    }

def xor_email(email: str) -> str:
    """XOR encodes email or password as required by some TikTok endpoints."""
    key = 5
    xored_email = []
    for c in email:
        xored_email.append(hex(ord(c) ^ key)[2:].zfill(2))
    return "".join(xored_email)



def get_base_params(config, ids):
    """
    Builds the exact base query parameters used by TikTok.
    """
    ts = int(time.time())
    app = config["app"]
    dev = config["device"]
    
    return {
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "_rticket": str(int(ts * 1000)),
        "cdid": ids["cdid"],
        "channel": app["channel"],
        "aid": str(app["aid"]),
        "app_name": app["app_name"],
        "version_code": str(app["version_code"]),
        "version_name": app["version_name"],
        "manifest_version_code": str(app["manifest_version_code"]),
        "update_version_code": str(app["update_version_code"]),
        "ab_version": app["version_name"],
        "resolution": "*".join(sorted(dev["resolution"].split('*'), key=int)),
        "dpi": str(dev["density_dpi"]),
        "device_type": dev["device_model"],
        "device_brand": dev["device_brand"].lower(),
        "language": "en",
        "os_api": str(dev["os_api"]),
        "os_version": dev["os_version"],
        "ac": "wifi",
        "is_pad": "0",
        "app_type": "normal",
        "sys_region": dev["sys_region"].upper(),
        "last_install_time": str(ids["apk_first_install_time"] // 1000),
        "mcc_mnc": dev["mcc_mnc"],
        "timezone_name": dev["timezone_name"],
        "carrier_region_v2": dev["mcc_mnc"][:3],
        "app_language": "en",
        "carrier_region": dev["sim_region"].upper(),
        "timezone_offset": str(dev["timezone_offset"]),
        "host_abi": "arm64-v8a",
        "locale": "en",
        "ac2": "wifi5g",
        "uoo": "0",
        "op_region": dev["sim_region"].upper(),
        "build_number": app["build_number"],
        "region": dev["sys_region"].upper(),
        "ts": str(ts),
        "openudid": ids["openudid"],
        "cronet_version": "3a9f3ddf 2026-06-25",
        "ttnet_version": "4.2.243.57-tiktok",
        "use_store_region_cookie": "1"
    }

def get_network_ua(config):
    app = config["app"]
    dev = config["device"]
    cronet_val = "3a9f3ddf 2026-06-25"
    quic_val = "c3b23989 2026-06-25"
    
    return (
        f"com.zhiliaoapp.musically/{app['update_version_code']} "
        f"(Linux; U; Android {dev['os_version']}; en; {dev['device_model']}; "
        f"Build/{dev['rom']}; Cronet/TTNetVersion:{cronet_val} QuicVersion:{quic_val})"
    )

def get_base_headers(config):
    """Returns headers common to all requests"""
    dev = config["device"]
    return {
        "x-tt-request-tag": "t=0;n=1", 
        "sdk-version": "2", 
        "passport-sdk-version": "1",
        "x-vc-bdturing-sdk-version": "2.4.2.i18n",
        "content-type": "application/json; charset=utf-8",
        "x-tt-app-init-region": f"carrierregion={dev['sim_region'].upper()};mccmnc={dev['mcc_mnc']};sysregion={dev['sim_region'].upper()};appregion={dev['sim_region'].upper()}",
        "x-ss-dp": str(config["app"]["aid"]), 
        "user-agent": get_network_ua(config), 
        "accept-encoding": "gzip, deflate, br"
    }

def inject_python_headers(headers, payload_for_sign, method, device_id, aid):
    """
    Calculates and injects the Python-side security headers (x-ss-stub, x-tt-trace-id, x-ss-req-ticket)
    expected by TikTok and required by the RapidAPI signer.
    """
    now_unix = time.time()
    req_ticket = str(int(now_unix * 1000))
    
    x_ss_stub = None
    if method.upper() == "POST":
        if payload_for_sign is not None and payload_for_sign != "":
            if isinstance(payload_for_sign, str):
                payload_encoded = payload_for_sign.encode('utf-8')
            else:
                payload_encoded = payload_for_sign
            x_ss_stub = hashlib.md5(payload_encoded).hexdigest().upper()
        else:
            x_ss_stub = hashlib.md5(b"").hexdigest().upper()
            
    if not device_id or device_id == "0":
        trace_str = (
            str("%x" % (round(now_unix * 1000) & 0xffffffff))
            + "10"
            + "".join(random.choice('0123456789abcdef') for _ in range(16))
        )
    else:
        trace_str = (
            hex(int(device_id))[2:]
            + "".join(random.choice('0123456789abcdef') for _ in range(2))
            + "0"
            + hex(int(aid))[2:]
        )
    trace_id = f"00-{trace_str}-{trace_str[:16]}-01"

    headers['x-ss-req-ticket'] = req_ticket
    headers['x-tt-trace-id'] = trace_id
    if x_ss_stub:
        headers['x-ss-stub'] = x_ss_stub
        
    return headers
