<span style="color:red">some **This is Red Bold.** text</span>

# Cloudflare Uam Bypass

### Additional Informations
 - The proxies type are `http,https` ...
 - You need fast proxies without this, the script will be **unstable**

### Installation
Install the app on the server
```sh
user@domain:~# git clone https://github.com/inplex-sys/cloudflare-uam-bypass.git
user@domain:~# cd ./cloudflare-uam-bypass/
user@domain:~# pip3 install Pysocks colored undetected_chromedriver
user@domain:~# python3 ./main.py <target> <threads> <proxies-file>
```

### Disclamer
This repository is for academic purposes, the use of this software is your responsibility.
