from gemini import Gemini
import time

cookies = {
    "__Secure-1PSIDCC" : "AKEyXzUdF9aVQQfRYWL4B4ftbqd2qjb5pafqPQxR3xPXAJuw-XYyPWEVwn0VSQd1UWqDrSgveFw",
    "__Secure-1PSID" : "g.a000kQgkE1LO2xzjL-tx3T7wC4PVb0pl9IBdUFK6rjqoikbM_ilurE7Cgu6mrNqz24pCbJuzawACgYKAW8SARYSFQHGX2Mi-xYI2lxac9hs-ybgRLPUfBoVAUF8yKq4Z4L-QsJlvcz_TSWrQwNo0076",
    "__Secure-1PSIDTS" : "sidts-CjIB3EgAEl1embiFYcNKEFlBCfoAgib7Mcc6vHi-kFllOWMm-lZYL4dqaZpU2jIjNXyioRAA",
    "NID" : "515=d-xa15pHZKk50NkCW3PpGyDMDxojRRP2I_AuTKkZO1qkBT_1u-vMI6MFpLjh4ZBBLgwFro1k4PTlpDjkMcNRywCWz5gm0Pb-BsnAYofFyy8R_4jveRj5XXBzhWn54Al1gIs-P6lkMDNPINaAtiL9mr8yXwREuACesyU6NYL8Vx7Bn5eEGIyC3xFbcR6Be_iwKn-U4-DxZauo648GdXRqz83P_oro7SFLQ8ElowzhF3nuvd8DtnGfsx5EkiKtZUC4X-pIMaL_TsgOCvVDf8WrCJBrFD5PUPR4c75kL68vRukS_64KQLkXeG66s7xEM_yEsC-F7aXVhM62oozvhCRJkTkP7o5NcyXKHROQhNf4l4u67CO3sPNMfrDCKis8q9FjNA",
    # Cookies may vary by account or region. Consider sending the entire cookie file.
  }
client = Gemini(cookies=cookies)

#client = Gemini(cookie_fp="/home/bessie/Downloads/cookies.txt") # (*.json, *.txt) are supported.

prompt="Como me llamo?"
#response = client.generate_content(prompt)
#print(response.payload)

response_text, response_status = client.send_request(prompt)
#print(response_text)
response = response_text

#response = client.generate_content(prompt)
#print(response.text)
#print(response.candidates)

#print(response[:100])
#print(type(response))

"""
for chunk in response10:
  print(chunk.text)
  print("_"*80)
"""
 
resp = response.replace('\n', '')
resp = response.replace('\\\\n', '')
resp = resp.replace('\r', '')
#resp = resp.replace('?', '')
resp = resp.replace('null,', '')
text = resp[150:500]

substring = "rc_"
result = ''

parts = text.split(substring, 1)
if len(parts) > 1:
    result = parts[1]
    #print(result)  # Output: the part you need]
else:
    print("Substring not found")
    
substring2 = ",["
result2 =''

parts = result.split(substring2, 1)
if len(parts) > 1:
    result2 = parts[1][2:]
    #print(result2)  # Output: the part you need]
else:
    print("Substring not found")
  
parts = result2.split("]", 1)  
result3 = parts[0][:-2]
print(result3)  # Output: the part you need]

 
    
#print(text)




