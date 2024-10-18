from sstc_core.sites.spectral import utils


def compute_qflag(
    latitude_dd: float,
    longitude_dd: float, 
    records_dict: dict,    
    timezone_str: str = 'Europe/Stockholm',
    is_per_image: bool = False, 
    default_temporal_resolution: bool = True  # default temporal resolution is 30 min, else 1 hr or more
) -> dict:
    """
    Computes the QFLAG and weight based on the given parameters.
    
    Parameters
    ----------
    latitude_dd : float
        Latitude in decimal degrees.
    longitude_dd : float
        Longitude in decimal degrees.
    records_dict : dict
        A dictionary containing records with 'creation_date' as one of the keys.
    timezone_str : str, optional
        The timezone string, by default 'Europe/Stockholm'.
    is_per_image : bool, optional
        If True, the number of records will not be considered in the QFLAG calculation, by default False.
    default_temporal_resolution : bool, optional
        If True, uses a default temporal resolution of 30 minutes, otherwise 1 hour or more, by default True.

    Returns
    -------
    dict
        A dictionary containing 'QFLAG' and 'weight'.
    """
    
    
    datetime_list = [v['creation_date'] for _, v in records_dict.items()]
    
    mean_datetime_str = utils.mean_datetime_str(datetime_list=datetime_list)
    sun_position = utils.calculate_sun_position(
        datetime_str=mean_datetime_str, 
        latitude_dd=latitude_dd, 
        longitude_dd=longitude_dd, 
        timezone_str=timezone_str
    )
    
    sun_elevation_angle = sun_position['sun_elevation_angle']
    solar_elevation_class = utils.get_solar_elevation_class(sun_elevation=sun_elevation_angle)
   
    n_records = len(records_dict)
        
    if (n_records < (3 if default_temporal_resolution else 2)) and (solar_elevation_class == 1):
        QFLAG = 11
        weight = 0.1 if not is_per_image else 0.5
        
    elif (n_records < (3 if default_temporal_resolution else 2)) and (solar_elevation_class == 2):
        QFLAG = 12
        weight = 0.75 if not is_per_image else 0.75
            
    elif (n_records < (3 if default_temporal_resolution else 2)) and (solar_elevation_class == 3):
        QFLAG = 13
        weight = 0.75 if not is_per_image else 1.0
            
    elif ((n_records >= (3 if default_temporal_resolution else 2)) and 
          (n_records < (6 if default_temporal_resolution else 4))) and (solar_elevation_class == 1):
        QFLAG = 21
        weight = 0.5
        
    elif ((n_records >= (3 if default_temporal_resolution else 2)) and 
          (n_records < (6 if default_temporal_resolution else 4))) and (solar_elevation_class == 2):
        QFLAG = 22
        weight = 0.75
  
    elif ((n_records >= (3 if default_temporal_resolution else 2)) and 
          (n_records < (6 if default_temporal_resolution else 4))) and (solar_elevation_class == 3):
        QFLAG = 23
        weight = 1
  
    elif (n_records >= (6 if default_temporal_resolution else 4)) and (solar_elevation_class == 1):
        QFLAG = 31
        weight = 0.75
        
    elif (n_records >= (6 if default_temporal_resolution else 4)) and (solar_elevation_class == 2):
        QFLAG = 32
        weight = 1.0
        
    elif (n_records >= (6 if default_temporal_resolution else 4)) and (solar_elevation_class == 3):
        QFLAG = 33
        weight = 1
        
    else:
        raise ValueError("Invalid input combination for n_records and solar_elevation_class")

    return {
        'QFLAG': QFLAG, 
        'weight': weight,
        'default_temporal_resolution': default_temporal_resolution,
        'is_per_image': is_per_image}

    

        
        