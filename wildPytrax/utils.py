# Internal functions

import requests
import os
import datetime as dt
import platform
import sys
from urllib.parse import urljoin

def _wt_authorization():
    """Wildtrax access token

    """

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

    ## If success, add message
    print("Authentication into WildTrax successful.")

    # Time until token expires
    now = dt.datetime.now()
    expiry_time = now + dt.timedelta(seconds=token_details['expires_in'])

    return token_details


def _wt_api_general(path, payload):
    """A function to handle general api requests
    """
    # get the auth token
    token = _wt_authorization()['access_token']
    user_agent = "Python/{} ({}; {} {})".format(
      platform.python_version(),
      platform.system(),
      platform.machine(),
      platform.version()
      )

    head = {'Authorization': f"Bearer {token}", 'User-Agent':user_agent}
    request = requests.post(url=urljoin("https://www-api.wildtrax.ca", '/bis/get-download-summary'), data=payload, headers = head)
    return request.json()
    
