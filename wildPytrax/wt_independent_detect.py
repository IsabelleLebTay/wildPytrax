def wt_indent_detect(x, threshold, units = "minutes",  datetime_col = date_detected, remove_human = True, remove_domestic = True):
     """Evaluate independent detections in your camera data

    Params:
    ------
    x: A dataframe of camera data; preferably, the output of `wt_download_report()`.
    threshold: int; time interval to parse out independent detections.
    units: string; The threshold unit. Can be one of three values, "seconds", "minutes", "hours".
    datetime_col: Defaults to `date_detected`; The column indicating the timestamp of the image.
    remove_human: Boolean; Should human and human-related tags (e.g. vehicles) be removed? Defaults to TRUE.
    remove_domestic: Boolean; Should domestic animal tags (e.g. cows) be removed? Defaults to TRUE.
    
    Usage:
    ------
    >>> Create independent detections dataframe using camera data from WildTrax

    """   
    