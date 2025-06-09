import json
import requests
import re
import random
import urllib.parse
import string

# Assuming 'cookies' is defined somewhere
cookies = {
    "__Secure-1PSIDCC" : "AKEyXzWHjArPSjNnRHMmuqCKqfHOdU6-ayyC0_KUo0y1b4KFUA7SqD9ueOSAJ1jCpsxwA8K6dPs",
    "__Secure-1PSID" : "g.a000kQgkE1LO2xzjL-tx3T7wC4PVb0pl9IBdUFK6rjqoikbM_ilurE7Cgu6mrNqz24pCbJuzawACgYKAW8SARYSFQHGX2Mi-xYI2lxac9hs-ybgRLPUfBoVAUF8yKq4Z4L-QsJlvcz_TSWrQwNo0076",
    "__Secure-1PSIDTS" : "sidts-CjIB3EgAEgK1YEMcuv9AJ0-IsyxwRXCYGntSIZ9UZnbULn4mQ91wcwI5qTZokcCPTzenYxAA",
    "NID" : "515=d-xa15pHZKk50NkCW3PpGyDMDxojRRP2I_AuTKkZO1qkBT_1u-vMI6MFpLjh4ZBBLgwFro1k4PTlpDjkMcNRywCWz5gm0Pb-BsnAYofFyy8R_4jveRj5XXBzhWn54Al1gIs-P6lkMDNPINaAtiL9mr8yXwREuACesyU6NYL8Vx7Bn5eEGIyC3xFbcR6Be_iwKn-U4-DxZauo648GdXRqz83P_oro7SFLQ8ElowzhF3nuvd8DtnGfsx5EkiKtZUC4X-pIMaL_TsgOCvVDf8WrCJBrFD5PUPR4c75kL68vRukS_64KQLkXeG66s7xEM_yEsC-F7aXVhM62oozvhCRJkTkP7o5NcyXKHROQhNf4l4u67CO3sPNMfrDCKis8q9FjNA",
    # Cookies may vary by account or region. Consider sending the entire cookie file.
  }

url = "https://gemini.google.com/app"
response = requests.get(url, cookies=cookies)
sid = re.search(r'"FdrFJe":"([\d-]+)"', response.text).group(1)
nonce = re.search(r'"SNlM0e":"(.*?)"', response.text).group(1)

reqid = int("".join(random.choices(string.digits, k=7)))

url_params = {
    "bl": "boq_assistant-bard-web-server_20240227.13_p0", # This will be changed as it updated.
    "hl": "en", # You can replace language. Refer README.md.
    "_reqid": reqid,
    "rt": "c",
    "f.sid": sid,
}

params = urllib.parse.urlencode(url_params)

data = {
    "at": nonce,
    "f.req": json.dumps([None, json.dumps([["How can I use you. what can you do?"], None, None and None])]), # Prompt and data structure.
}

data_encoded = urllib.parse.urlencode(data)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "*/*",
    "Referer": "https://gemini.google.com/",
    "X-Same-Domain": "1",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    "Origin": "https://gemini.google.com",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

response10 = requests.post(
    "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
    params=params,
    cookies=cookies,
    headers=headers,
    data=data_encoded,
)

print(response10.text[:100])
print(response10.status_code)
print(type(response10.text))

"""
for chunk in response10:
  print(chunk.text)
  print("_"*80)
"""
 
resp = response10.text.replace('\n', '')
resp = resp.replace('\r', '')
resp = resp.replace('?', '')
print(resp)


     
