from ..io_tools import load_yaml
from pathlib import Path

stations_dirpath = Path(__file__).parent
spectral_dirpath = Path(stations_dirpath).parent
config_dirpath = spectral_dirpath / "config"
catalog_db_filepath = config_dirpath / "catalog_db_filepaths.yaml"

meta = {
    "version": '2024_v0.3',
    "station_acronym": "RBD",
    "long_station_name": "Röbäcksdalen Field Research Station",
    "is_active": True,
    "station_name": "Röbäcksdalen",
    "normalized_station_name": "robacksdalen",    
    "locations_filepath": config_dirpath / 'locations' / 'locations_robacksdalen.yaml',
    "platforms_filepath": config_dirpath / 'platforms' / 'platforms_robacksdalen.yaml',
    "phenocam_quality_weights_filepath": config_dirpath / "phenocam_quality_weights.yaml",    
    'geolocation':{
        'point':{ 
          'epsg': "epsg:4326",
          'latitude_dd': 63.81083,
          'longitude_dd': 20.24199,
    }
    } 
    }

def load_configurations():
    """
    Loads configurations for the Abisko station from YAML files.

    Returns:
      tuple: A tuple containing locations and platforms configuration data.
    """
    # Loading station locations config
    locations = load_yaml(meta["locations_filepath"])

    # Loading station platforms config
    platforms = load_yaml(meta["platforms_filepath"])

    return locations, platforms


locations, platforms = load_configurations()


    

