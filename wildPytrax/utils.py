# Internal functions

# Wildtrax authentification

import requests
import os
import datetime as dt

def _wt_authorization():

    bytelist = ['0x45', '0x67', '0x32', '0x4d', '0x50', '0x56', '0x74', '0x71', '0x6b',
             '0x66', '0x33', '0x53', '0x75', '0x4b', '0x53', '0x35', '0x75', '0x58', '0x7a', '0x50',
             '0x39', '0x37', '0x6e', '0x78', '0x55', '0x31', '0x33', '0x5a', '0x32', '0x4b', '0x31',
             '0x69']

    cid= ''.join([chr(int(x.encode('utf-8'), 16)) for x in bytelist])
    url = 'https://abmi.auth0.com/oauth/token'

    payload = {
        'audience' : "http://www.wildtrax.ca",
        'grant_type' : "password",
        'client_id' : cid,
        'username': os.environ['USRNAME'],
        'password': os.environ['PWD']
    }

    token_details = requests.post(url, data=payload).json()

    ## Add error messages here if authentication failed

    # Time until token expires
    now = dt.datetime.now()
    expiry_time = now + dt.timedelta(seconds=token_details['expires_in'])

    return token_details

_wt_authorization()
    