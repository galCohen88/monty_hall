import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64

"""
maintainer gal.nevis@gmail.com
based on https://developers.google.com/gmail/api/quickstart/python
first execution will need auth2 login with new token pickle file to be created using browser
begin with creating credentials.json file in order to create token.pickle file
"""

USER_ID = 'me'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    messages = service.users().messages().list(userId=USER_ID).execute()
    for message in messages.get('messages'):
        message_id = message.get('id')
        message = service.users().messages().get(userId=USER_ID, id=message_id).execute()
        message_content = message['payload']['parts'][0]['body']['data']
        raw_html = str(base64.urlsafe_b64decode(message_content), 'utf-8')
        print(raw_html)


if __name__ == '__main__':
    main()

