from gemini import Gemini

"""
client = Gemini(auto_cookies=True)

# Testing needed as cookies vary by region.
# client = Gemini(auto_cookies=True, target_cookies=["__Secure-1PSID", "__Secure-1PSIDTS"])
# client = Gemini(auto_cookies=True, target_cookies="all") # You can pass whole cookies

response = client.generate_content("Hello, Gemini. What's the weather like in Seoul today?")
print(response.payload)
"""
cookies = {
    "__Secure-1PSIDCC" : "AKEyXzWvTYXsgr1ixQRpse9dl6x_047KoxQskiqWi33pQqzK9xyjMAPcg2-q0r02oPHhOwGyYIgn",
    "__Secure-1PSID" : "g.a000kQgkE1LO2xzjL-tx3T7wC4PVb0pl9IBdUFK6rjqoikbM_ilurE7Cgu6mrNqz24pCbJuzawACgYKAW8SARYSFQHGX2Mi-xYI2lxac9hs-ybgRLPUfBoVAUF8yKq4Z4L-QsJlvcz_TSWrQwNo0076",
    "__Secure-1PSIDTS" : "sidts-CjIB3EgAEqvoq5IindGzncLdoOPQ3yB4oLisokIek7vjSoYV4vwqW7maEKCjcXKolX5aDRAA",
    "NID" : "514=Bo6iDqzS2qyWE2U3UlpGyQMxmidpfeUZTvuxqjuEMQNNVM5O75hKI0EXiGHEmSCUUI83cFHxCCNovMPE-ORmXWezX_2UqUCXJdG3jmKUX9J1li2HQmQ56kyE2X2u-TBSHV6Fo2QY4Th9hjiweNdUnNVxj8Hfkze4Ym5JSs5xO2tHkqSidDUzHPkmTmcfIm3mnyVD7yBjn3TzFYqVF9F3lWvEUz-h0Dtde9UhoUDACH7y77DRwuzYbspSP2eVSV0fBohEtQG6oKk20CE7hp1AEFGIy7vvzABHLghsnhcw8Rbky4E51qT9Hv3vM-tthDOwbA06D0gh18fyusb2RL8ycO0mW_WvnVKyN19jmy8-0TnCuH8Y34XsvX2iUAjDzIL1bw",
    # Cookies may vary by account or region. Consider sending the entire cookie file.
  }
  
"""
client = Gemini(cookies=cookies)

"""

client = Gemini(cookie_fp="/home/bessie/Downloads/cookies.txt") # (*.json, *.txt) are supported.

prompt = "Tell me about Large Language Model."
response = client.generate_content(prompt)
print(response.payload)

#response_text, response_status = client.send_request("Hola, dime sobre el tiempo")
#print(response_text)
"""
prompt = "Hello, Gemini. Tell me about Large Language Models."
response = client.generate_content(prompt)
print(response.text)
"""
