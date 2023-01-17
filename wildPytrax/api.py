import pandas as pd

def wt_auth():
    """Authenticate into WildTrax
    Usage:
    >> Obtain Auth0 credentials using WT_USERNAME and WT_PASSWORD stored from a config file, or .env
    """
    return _wt_authorization()

def wt_get_download_summary(sensor):
    """Obtain a dataframe listing projects that the user is able to download data for

    Params:
    sensor: "ARU" or "CAM"
    """
    response = _wt_api_general(path ="/bis/get-download-summary", payload={'sensorId': str(sensor),'sort' : "fullNm",'order' : "asc"})

    df = pd.DataFrame(response['results'], columns=['fullNm', 'id', 'sensorId', 'tasks', 'status'])
    df.rename(columns={'fullNm': 'Project', 'id' : 'projectId'}, inplace=True)

    return df