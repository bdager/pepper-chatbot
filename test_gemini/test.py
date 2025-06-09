from gemini import Gemini

#client = Gemini(auto_cookies=True)

# Testing needed as cookies vary by region.
#client = Gemini(auto_cookies=True, target_cookies=[_Secure_1PSID, _Secure_1PSIDTS])
# client = Gemini(auto_cookies=True, target_cookies="all") # You can pass whole cookies

cookies = {
    "__Secure-1PSIDCC" : "AKEyXzX0m-GTAdENTJsgnNOBL-4myBlCYr1qTqKR_bNVCH4ee0dZAvNVv_Cv1wTIILwUncLEGHc",
    "__Secure-1PSID" : "g.a000kQgkE1LO2xzjL-tx3T7wC4PVb0pl9IBdUFK6rjqoikbM_ilurE7Cgu6mrNqz24pCbJuzawACgYKAW8SARYSFQHGX2Mi-xYI2lxac9hs-ybgRLPUfBoVAUF8yKq4Z4L-QsJlvcz_TSWrQwNo0076",
    "__Secure-1PSIDTS" : "sidts-CjIB3EgAEg4MSiuLFkI4RahBJeJDDHm-RikvAmK6IV2cKcIYmHXox-bq4_B6ElIfaumM3xAA",
    "NID" : "514=kfv22cYx-6tTnwUNih5jaBL70tWG1Z_OHcsNR0pj4Jp-Cyjvvr2Cn6RUjp5Pi1JNAfiZ33A6uGEweMIcBXoJaIeB77KyzGKujJsUpPO4ifwooH62S90ghx13u2TP7n3GZYfUXr5Y4N6JqCDZ8nJODXKATOpw7yHntEAAag-jFNRm_TZAOt0xowFl1a3RlLmHzXfC0WqdInydm6RitP3zNiaAcJUrp6g7J2cug3dd0ssaynZhHIzbvvzZ6jlLT-YIz4JLUiLx16j00hOse82A_5U6OqKFBoY3r3d8RiGhe6Bou9aiX0DSJRhlqtafbMnMtmpHVLBHcOuH6imbqImmYfMWj4f3D17XAE3pC6vcLn_9QYTnV54tkrPjuVW8_R5Ylg",
    # Cookies may vary by account or region. Consider sending the entire cookie file.
  }

client = Gemini(cookies=cookies)


#prompt = "Tell me about Large Language Model."
#response = client.generate_content(prompt)
#print(response.payload)

response_text, response_status = client.send_request("Hola, dime sobre el tiempo")
print(response_text)
