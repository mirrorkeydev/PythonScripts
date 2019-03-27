""" 
A command-line tool that scrapes the Appstract request email inbox for all requests.
The tool performs an analysis on all apps requested, and then outputs the ones with 
the highest number of requests. Adapted from Gmail's API sample code.
Note that this tool requires a user to login to the email inbox they'd like to scrape;
as such, it can be used by anybody, but the functionality won't work unless your inbox
happens to be filled with request emails generated by CandyBar Dashboard.
"""

"""
TODO:
-create dictionary to track frequency of icon names
-figure out how to get more than the first 40 emails from the inbox
-make extracting the payload from the message more reliable (aka remove try/excepts)
"""

from __future__ import print_function
import pickle
import os.path
import base64
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getRequestName(decoded_payload):
    #find the first requested icon name, using "CandyBar Version" to detect if it's a request email
    if "CandyBar Version" in decoded_payload:
        tempstr = ""
        start = -1
        count = 0
        match = re.search("CandyBar Version[ \n]: \d.\d.\d-b4(\\\\n){1,3}", decoded_payload)

        if match is not None:
            #determines the location of the first letter of an icon
            start = match.span()[1]

            #interate from first letter to terminating "\n" or 20 characters, whichever comes first
            currentchar = ""
            while not(count >= 20):
                currentchar = str(decoded_payload[start + count])

                #check for terminating "\n"
                if currentchar == "\\":
                    break

                tempstr += currentchar
                count += 1

            return(tempstr)

        if match is None:
            return("No match found")

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me').execute()

    for message in results["messages"]:
        message_id = message["id"]
        
        #get an individual message by its id
        individual_message = service.users().messages().get(userId='me', id=str(message_id), format="full").execute()

        #check if this is a request email
        if "CandyBar Version" in str(individual_message["snippet"]):
            #extract the body from the message, which is base64 encoded
            try:
                payload = individual_message["payload"]["parts"][0]["parts"][0]["body"]["data"]
            except:
                payload = individual_message["payload"]["parts"][0]["body"]["data"]

        #decode the payload, giving the plain text body of the email
        decoded_payload = str(base64.b64decode(payload, '-_')).replace("\\r","")

        #extract the name of the first request
        print(getRequestName(decoded_payload))
    
    
    # In case something goes horribly wrong, the below code is the outline of how the payload is extracted

    # Call the Gmail API
    #results = service.users().messages().list(userId='me').execute()

    #get an individual message by its id
    #message = service.users().messages().get(userId='me', id="169a039f23db5890", format="full").execute()

    #extract the body from the message, which is base64 encoded
    #payload = message["payload"]["parts"][0]["parts"][0]["body"]["data"]

    #decode the payload, giving the plain text body of the email
    #decoded_payload = str(base64.b64decode(payload, '-_')).replace("\\r","")


if __name__ == '__main__':
    main()