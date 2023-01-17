import requests
import datetime
import os
from urllib.parse import urljoin
import platform
import sys
import pandas as pd
import zipfile

def wt_auth():
    """Authenticate into WildTrax
    Usage:
    ------
    >> Obtain Auth0 credentials using WT_USERNAME and WT_PASSWORD stored from a config file, or .env

    """
    return _wt_authorization()

def wt_get_download_summary(sensor):
    """Obtain a dataframe listing projects that the user is able to download data for

    Params:
    ------
    sensor: string, "ARU" or "CAM"

    """
    response = _wt_api_general(path ="/bis/get-download-summary", payload={'sensorId': str(sensor),'sort' : "fullNm",'order' : "asc"})

    df = pd.DataFrame(response['results'], columns=['fullNm', 'id', 'sensorId', 'tasks', 'status'])
    df.rename(columns={'fullNm': 'Project', 'id' : 'projectId'}, inplace=True)

    return df

def wt_download_report(project_id, sensor_id, report, weather_cols = True):
    """Download ARU, Camera, or Point Count data from a project

    Params:
    ------
    project_id: int. the project ID number that you would like to download data for. Use `wt_get_download_summary()` to retrieve these IDs.
    sensor_id: string. Can either be "ARU", "CAM", or "PC".
    report: string. The report type to be returned. Multiple values are accepted as a concatenated string.
    weather_cols: Boolean. Do you want to include weather information for your stations? Defaults to TRUE.
    usage:
    ------
    >>>

    """
    dl_summary = wt_get_download_summary(sensor = sensor_id)

    project_line = dl_summary.loc[dl_summary['projectId'] == project_id]
    # print(project_line)
    if project_line.shape[0] == 0:
        print("The project_id you specified is not among the projects you are able to download for.")
        exit()

    # Allowable reports for each sensor
    cam = ["image", "tag", "megadetector", "definitions"]
    aru = ["summary", "birdnet", "task", "tag", "definitions"]
    pc = ["report", "definitions"]

    if (sensor_id == "CAM") and (report not in cam):
        print("Please supply a valid report type. Use ?wt_download_report to view options.")
        exit()
    if (sensor_id == "ARU") and (report not in aru):
        print("Please supply a valid report type. Use ?wt_download_report to view options.")
        pass
    if (sensor_id == "PC") and (report not in pc):
        print("Please supply a valid report type. Use ?wt_download_report to view options.")
        pass

    # Create the post request
    payload = {
        'projectIds' : project_id,
        'sensorId' : sensor_id,
        'splitLocation' : False}
    token = _wt_authorization()['access_token']
    headers = {'Authorization': f"Bearer {token}", 'User-Agent':_get_user_agent(), 'Accept': "application/zip"}
    response = requests.post(url=urljoin("https://www-api.wildtrax.ca", "/bis/download-report"),
     data = payload,
     headers=headers,
     stream=True)

    if response.status_code != 200:
        print("Error: {}\n{}".format(response.status_code, response.text))

    with open("tempFile.zip", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    # unzip tempfile and dump contents to new folder
    dir =str(project_line.iloc[0]['Project'])
    os.makedirs(dir)
    with zipfile.ZipFile("tempFile.zip","r") as zip_ref:
        # dir = os.makedirs(str(project_line.iloc[0]['Project']))
        zip_ref.extractall(dir)
        print(dir)
        print("here")

    # Remove abstract file
    abstract = [file for file in os.listdir(dir) if "abstract" in file][0]
    print(abstract)
    print(os.path.join(dir, abstract))
    os.remove(os.path.join(dir, abstract))

    # List files in new dir
    list_of_files = os.listdir(dir)

    # Remove weather columns, if desired

    # Return the requested report(s)
    # If multiple report types are requested, a list of dataframes is returned; if only one, a dataframe.
    if (type(report) == list) and (len(report) == 1):
        report = report[0]
        print('type is list, one item')
    if type(report) == str:
        report_df = pd.read_csv([file for file in os.listdir(dir) if str(report) in file][0])
        print('type is str')
    else:
        report_df = {}
        print('type is list, multiple items')
        for i in report:
            report_df[i] = pd.read_csv([file for file in os.listdir(dir) if str(i) in file][0])

    # Remove zip folder
    os.remove('tempFile.zip')

    return report_df