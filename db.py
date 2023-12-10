import requests
import urllib.parse
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import hashlib
import sys
import base64

def encrypt_string(text):
    password = 'Idontknow@1234'
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    encrypted_text = base64.b64encode(ciphertext).decode('utf-8')
    return f'{iv}${encrypted_text}'


def query(sql):
    url = "https://somethingisnothing.000webhostapp.com/dataQuery?sql="
    if not sql:
        return json.dumps({"success": False, "error": "query requires one argument"})
    sql = urllib.parse.quote(sql)
    sql = encrypt_string(sql)
    url += base64.b64encode(sql.encode()).decode('utf-8')
    r = requests.get(url)
    return json.loads(r.text)

if __name__ == "__main__":
    argus = sys.argv
    if len(argus) > 1:
        if argus[1] == "--interactive":
            inp = input("SQL Query: ")
            while inp != "exit":
                print(query(inp))
                inp = input("SQL Query: ")