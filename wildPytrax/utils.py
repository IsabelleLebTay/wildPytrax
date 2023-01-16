# Internal functions

# Wildtrax authentification

import requests
import os

def wt_authorization():
    """Login credential authorization

    Params:
    -----

    Usage:
    >>
    >>
    
    
    """
    cid = id
    request = requests.post(
        url = "https://abmi.auth0.com/oauth/token",
        encode = "form",
        body = list(
            audience = "http://www.wildtrax.ca",
            grant_type = "password",
            client_id = cid,
            username = os.getenv("WT_USERNAME"),
            password = os.getenv("WT_PASSWORD")
            )
        )