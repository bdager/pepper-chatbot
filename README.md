
You need to enter the __Secure-1PSID(named token in the code )and __Secure-1PSIDTS(start with: "sidts-...") cookies in the main file(at the end of the code). You'll find them by going to Bard in a web browser (Chrome, Firefox, etc.)connect with your google account, opening the console (f12), then looking for the cookies (on Chrome, go to "application") and they'll be there (note that the __Secure-1PSIDTS changes every time you close the browser).

Then, in the terminal you need to execute the command export PYTHONPATH=${PYTHONPATH}:<path_to_the_file>/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages

Besides execute python3 mainb.py and then choose your language.

If you have the message error : Exception: "SNlM0e value not found. Double-check __Secure-1PSID value or pass it as token='xxxxx'."
Refresh the Bard google page and retake the __Secure-1PSIDTS (normally the __Secure-1PSID doesn't change).



Here is a link to the BARD gitlab : https://github.com/dsdanielpark/Bard-API