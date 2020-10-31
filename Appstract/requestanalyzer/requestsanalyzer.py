""" 
A command-line tool that scrapes the Appstract request email inbox for all requests.
The tool performs an analysis on all apps requested, and then outputs the ones with 
the highest number of requests. Adapted from Gmail's API sample code.
Note that this tool requires a user to login to the email inbox they'd like to scrape;
as such, it can be used by anybody, but the functionality won't work unless your inbox
happens to be filled with request emails generated by CandyBar Dashboard.
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


"""
Function: get_request_code()
Parameters: decoded_payload - the body of a CandyBar request email
            start - the start index of an icon in decoded_payload
Returns: the associated icon identifier string of an icon
Purpose: For a given start index, find the identifier of an icon
"""
def get_request_code(decoded_payload, start):
    tempcode = ""
    count = 0
    currentchar = ""
    slash_n_found = False

    # iterate from first "\n" to second "\n" or 130 characters, whichever comes first
    while not(count > 130):
        try:
            currentchar = str(decoded_payload[start + count])

            # check for first "\n"
            if currentchar == "\\" and not slash_n_found:
                slash_n_found = True
                # increment to get ahead of "\n"s "n"
                count += 1
            
            # check for second "\n"
            elif currentchar == "\\" and slash_n_found:
                break

            # if the character is between the first and second "\n"
            elif slash_n_found:
                tempcode += currentchar
        except:
            return "Error parsing request code"

        count += 1
    
    return tempcode

"""
Function: get_request_names()
Parameters: decoded_payload, the body of a CandyBar request email
Returns: a list containing tuples in the form: ("Iconname", "Icon ID")
Purpose: Searches emails for the titles of icons that a user requested
"""
def get_request_names(decoded_payload):
    icon_match = re.finditer("(\\\\n){2,3}", decoded_payload)
    icons_iter = iter(icon_match)
    icons = []

    for i in range(len(re.findall("(\\\\n){2,3}", decoded_payload))):
        start = next(icons_iter).span()[1]
        
        if len(decoded_payload) - start < 10:
            # the \\n is too close to the end of the string, ignore it
            break

        tempstr = ""
        count = 0
        currentchar = ""

        # iterate from first letter to terminating "\n" or 20 characters, whichever comes first
        while not(count > 20):
            currentchar = str(decoded_payload[start + count])

            # check for terminating "\n"
            if currentchar == "\\":
                break
    
            tempstr += currentchar
            count += 1
    
        # sanity check that the icon has a name
        if tempstr != "":
            #fetch the icon identifier
            code = get_request_code(decoded_payload, start)
            tup = (tempstr, code)
            icons.append(tup)

    return icons


"""
Function: update_frequencies()
Parameters: icons - a list containing tuples in the form: ("Iconname", "Icon ID")
            icon_frequency - the frequency dictionary to be filled
Returns: n/a
Purpose: adds the icon key to a dictionary, updating the value if it already exists 
"""
def update_frequencies(icons, icon_frequency):
    # structure of an icon_frequency entry:
    #     "IconName":[iconfrequency, "Code1", "Code2", ...,]
    # ex: "Youtube":[3, "com.google.yt/youtube.Activity", "com.google.yt/youtube.SplashAct"]

    for icon in icons:
        if icon is not None:
            if icon[0] in icon_frequency:
                icon_frequency[icon[0]][0] += 1

            else:
                icon_frequency[icon[0]] = [1]
            
            if icon[1] not in icon_frequency[icon[0]]:
                icon_frequency[icon[0]].append(icon[1])
        
            # print the current icon and its corresponding frequency
            print("Icon: " + "{:25}".format(str(icon[0])) + "Frequency: " + str(icon_frequency[icon[0]][0]))
            

"""
Function: analyze_message()
Parameters: message - an individual message descriptor containing an email ID
            icon_frequency - the frequency dictionary to be filled
            service - the Gmail API resource
Returns: a boolean describing whether the message was an icon request email
Purpose: determines message validity and extracts the payload
"""
def analyze_message(message, icon_frequency, service):
    message_id = message["id"]
            
    # using the message id, retrieve the full email from the server
    individual_message = service.users().messages().get(userId='me', id=str(message_id), format="full").execute()

    # check if this email is a free request email
    if "CandyBar Version" in str(individual_message["snippet"]) and "Order Id" not in str(individual_message["snippet"]):
        # extract the body from the message, which is base64 encoded
        try:
            payload = individual_message["payload"]["parts"][0]["parts"][0]["body"]["data"]
        except:
            try:
                payload = individual_message["payload"]["parts"][0]["body"]["data"]
            except:
                return False

        # decode the payload, giving the plain text body of the email
        decoded_payload = str(base64.b64decode(payload, '-_')).replace("\\r","")
        
        # extract the names of the icon requests
        icons = get_request_names(decoded_payload)

        # update the frequency dictionary
        update_frequencies(icons, icon_frequency)

        return True
    
    return False


"""
Function: top_requests()
Parameters: icon_frequency, the dictionary of "IconName": frequency
Returns: n/a
Purpose: prints the top x requested icons
"""
def top_requests(icon_frequency):
    # next, linearly search for the x most requested icons
    x = 0
    while(True):
        x = int(input("View the top x requested icons. x = "))
        if x < len(icon_frequency):
            break
        print("x too large! Pick an x less than " + str(len(icon_frequency)))

    maxkey = ""
    ls = []

    # loop x times
    for i in range(x):
        maxkey = ""
        maxval = 0
        maxinfo = ""

        # loop through the dictionary's items
        for key, value in icon_frequency.items():
            if value[0] > maxval:
                tup = (key, value)

                # makes sure that the icon hasn't already been added to the top x
                if tup not in ls:
                    maxkey = key
                    maxval = value[0]
                    maxinfo = value 
        temptuple = (maxkey, maxinfo)
        ls.append(temptuple)

    # print results
    print("TOP " + str(x) + " ICONS:")

    for item in ls:
        print("-------------------------------------------------------")
        print("Icon: " + "{:25}".format(str(item[0])) + "Requested: " + "{:5}".format(str(item[1][0])))
        for i in range(1,len(item[1])):
            print("<item component=\"ComponentInfo{" + item[1][i] + "}\" drawable=\"" + str(item[0].lower().replace(" ", "_")) + "\"/>")

    print("Total number of icons requested: " + str(len(icon_frequency)))


"""
Function: get_credentials()
Parameters: n/a
Returns: the credentials needed to call the Gmail API
Purpose: retrieves stored credentials or asks the user to login to the Gmail account 
"""
def get_credentials():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
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
        
    return creds


"""
Function: main()
Parameters: n/a
Returns: n/a
Purpose: driving code of the program; executes all functions 
""" 
def main():

    # retrieve credentials
    creds = get_credentials()

    # create an API resource to interact with
    service = build('gmail', 'v1', credentials=creds)

    # call the Gmail API, retrieving the first page of emails
    # note:
    response = service.users().messages().list(userId="me").execute()

    # store those emails, then iterate through and store the subsequent pages of emails
    messages = []
    if "messages" in response:
        messages.extend(response["messages"])
    
    while "nextPageToken" in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId="me", pageToken=page_token).execute()
        messages.extend(response['messages'])

    # now that we have all the emails, ask the user how many they'd like to process
    while(True):
        custom = int(input("Enter the x most recent emails to analyze out of " + str(len(messages)) + ", or enter -1 to analyze all emails. x = "))
        if custom <= len(messages):
            break
        print("You don't have that many emails to analyze. Try a smaller amount.")
    
    icon_frequency = {}
    invalid_email_streak = 0

    # if the user opts for all of the emails in the inbox, do so
    # note that this loop automatically terminates if too many emails in a row aren't requests
    # this tolerance can be raised by editing the tolerance variable below
    if custom == -1:

        # if more than 15 emails in a row don't conform, the loop exits
        tolerance = 15

        for message in messages:
            success = analyze_message(message, icon_frequency, service)
            if success:
                invalid_email_streak = 0
            elif not success:
                invalid_email_streak += 1
            if invalid_email_streak > tolerance:
                break

    # else, only analyze in a custom range, starting with the most recent emails
    else:
        for i in range(custom):
            success = analyze_message(messages[i], icon_frequency, service)

    # analyze a user-defined amount of top requests from the icon_frequency dictionary
    top_requests(icon_frequency)

if __name__ == '__main__':
    main()