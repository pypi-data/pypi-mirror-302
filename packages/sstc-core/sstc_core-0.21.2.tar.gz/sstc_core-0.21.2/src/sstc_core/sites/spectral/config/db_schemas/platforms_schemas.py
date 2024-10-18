import os
from typing import List, Dict, Any
from sstc_core.sites.spectral.data_products.phenocams import config_flags_yaml_filepath, get_default_phenocam_flags
from sstc_core.sites.spectral.stations import Station


def build_phenocams_rois_flags_schema(station: Station, platform_id: str,  phenocam_flags_dict:dict, platforms_type:str = 'PhenoCams'  )->list:
    
    phenocam_rois_dict = station.phenocam_rois(
        platforms_type=platforms_type,
        platform_id=platform_id
        )
    
    fields_list = []
    
    suffixes = phenocam_flags_dict.keys()

    if phenocam_rois_dict:
        for r in phenocam_rois_dict.keys():
            for suffix in suffixes:
                field_name = f'{r}_{suffix}'            
                field_default_value = False
                field_type = 'BOOLEAN'

                fields_list.append({
                    'field_name': field_name,
                    'field_type': field_type,
                    'field_default_value': field_default_value
                })                
    return fields_list
 

def __build_phenocams_rois_parameters_schema(
    station: Station, 
    platform_id: str, 
    parameters_dict: dict,
    default_field_type: str,  # Options: 'BOOLEAN', 'VARCHAR', 'INTEGER', 'DOUBLE'
    custom_field_types: dict = None,
    platforms_type: str = 'PhenoCams',
    prefix: str = '',  
) -> list:
    """
    Builds a schema for PhenoCams ROI parameters by generating a list of dictionaries containing field information.

    Parameters
    ----------
    station : Station
        An instance of the Station class containing phenocam ROIs.
    platform_id : str
        The identifier of the platform.
    platforms_type : str, optional
        The type of platform, by default 'PhenoCams'.
    prefix : str, optional
        A prefix to prepend to field names, by default ''.
    parameters_dict : dict, optional
        A dictionary of parameters and their default values, by default None.
        Example: {'num_pixels': None, 'SUM_Red': None, 'SUM_Green': None, 'SUM_Blue': None}
    default_field_type : str, optional
        Options include 'BOOLEAN', 'VARCHAR', 'INTEGER', 'DOUBLE'.
    custom_field_types : dict, optional
        A dictionary to specify custom field types, by default None.
        Example: {'num_pixels': 'INTEGER'}

    Returns
    -------
    list
        A list of dictionaries where each dictionary represents a field with 'field_name', 'field_type', and 'field_default_value'.

    Raises
    ------
    ValueError
        If `platform_id` is not provided.
        If `phenocam_rois_dict` is empty.

    Examples
    --------
    >>> station = Station()  # Assume this is a properly initialized Station object
    >>> schema = __build_phenocams_rois_parameters_schema(
    ...     station=station,
    ...     platform_id='XYZ123',
    ...     prefix='phenocam',
    ...     parameters_dict={'num_pixels': 0, 'SUM_Red': 0, 'SUM_Green': 0, 'SUM_Blue': 0},
    ...     default_field_type='DOUBLE',
    ...     custom_field_types={'num_pixels': 'INTEGER'}
    ... )
    >>> print(schema)
    [{'field_name': 'phenocam_1_num_pixels', 'field_type': 'INTEGER', 'field_default_value': 0}, ...]
    """
    if not platform_id:
        raise ValueError("The 'platform_id' must be provided.")
    
    if parameters_dict is None or len(parameters_dict) == 0:
        raise ValueError("The 'parameters_dict' must be provided.")
        
    
    phenocam_rois_dict = station.phenocam_rois(
        platforms_type=platforms_type,
        platform_id=platform_id
    )

    if not phenocam_rois_dict:
        raise ValueError(f"No ROIs found for platform_id: {platform_id} with platforms_type: {platforms_type}")

    fields_list = []
    suffixes = parameters_dict.keys()

    for roi_key in phenocam_rois_dict.keys():
        for suffix in suffixes:
            field_name = f'{prefix}_{roi_key}_{suffix}'            
            field_value = parameters_dict[suffix]
            field_type = custom_field_types.get(suffix, default_field_type)

            fields_list.append({
                'field_name': field_name,
                'field_type': field_type,
                'field_default_value': field_value 
            })
    
    return fields_list
    

from typing import List

def build_phenocams_rois_L2_parameters(
    station: Station, 
    platform_id: str, 
    platforms_type: str = 'PhenoCams',
    prefix: str = 'L2',  
    parameters_dict: dict = {
        'num_pixels': None,
        'SUM_Red': None,
        'SUM_Green': None,
        'SUM_Blue': None,
    }, 
    default_field_type: str = 'DOUBLE',  # Options: 'BOOLEAN', 'VARCHAR', 'INTEGER', 'DOUBLE'
    custom_field_types: dict = {'num_pixels': 'INTEGER'}
) -> List[dict]:
    """
    Builds L2 parameter schema for PhenoCams ROI data.

    This function generates a schema for Level 2 (L2) PhenoCams ROI parameters by leveraging the 
    internal helper function `__build_phenocams_rois_parameters_schema`. The generated schema is a list 
    of dictionaries, each containing information about a specific field required for storing PhenoCams ROI data.

    Parameters
    ----------
    station : Station
        An instance of the Station class containing phenocam ROIs.
    platform_id : str
        The identifier of the platform.
    platforms_type : str, optional
        The type of platform, by default 'PhenoCams'.
    prefix : str, optional
        A prefix to prepend to field names, by default 'L2'.
    parameters_dict : dict, optional
        A dictionary of parameters and their default values, by default:
        {
            'num_pixels': None,
            'SUM_Red': None,
            'SUM_Green': None,
            'SUM_Blue': None,
        }
    default_field_type : str, optional
        The default field type to use, by default 'DOUBLE'. 
        Options include 'BOOLEAN', 'VARCHAR', 'INTEGER', 'DOUBLE'.
    custom_field_types : dict, optional
        A dictionary to specify custom field types, by default {'num_pixels': 'INTEGER'}.

    Returns
    -------
    List[dict]
        A list of dictionaries where each dictionary represents a field with 'field_name', 'field_type', and 'field_default_value'.

    Examples
    --------
    >>> station = Station()  # Assume this is a properly initialized Station object
    >>> L2_schema = build_phenocams_rois_L2_parameters(
    ...     station=station,
    ...     platform_id='XYZ123',
    ...     prefix='L2',
    ...     parameters_dict={'num_pixels': 0, 'SUM_Red': 0, 'SUM_Green': 0, 'SUM_Blue': 0},
    ...     default_field_type='DOUBLE',
    ...     custom_field_types={'num_pixels': 'INTEGER'}
    ... )
    >>> print(L2_schema)
    [{'field_name': 'L2_1_num_pixels', 'field_type': 'INTEGER', 'field_default_value': 0}, ...]
    """
    return __build_phenocams_rois_parameters_schema(
        station=station,
        platform_id=platform_id,
        platforms_type=platforms_type,
        prefix=prefix,
        parameters_dict=parameters_dict,
        default_field_type=default_field_type,
        custom_field_types=custom_field_types,
    )
    
    
def build_phenocams_rois_L3_parameters(
    station: Station, 
    platform_id: str, 
    platforms_type: str = 'PhenoCams',
    prefix: str = 'L3',  
    parameters_dict: dict = {
        'has_snow_presence': False,        
        'QFLAG_value': None,
        'QFLAG_weight': None,
        'num_pixels': None,
        'SUM_Red': None,
        'SUM_Green': None,
        'SUM_Blue': None,
        'MEAN_Red': None,
        'MEAN_Green': None,
        'MEAN_Blue': None,        
        'SD_Red': None,
        'SD_Green': None,
        'SD_Blue': None,
        'MEANS_RGB_SUM': None,
        'GCC_daily_value': None,
        'RCC_daily_value': None,
        'weighted_MEAN_Red': None,
        'weighted_MEAN_Green': None,
        'weighted_MEAN_Blue': None, 
        'has_iflags': False,      
    },
       
    default_field_type: str = 'DOUBLE',  # Options: 'BOOLEAN', 'VARCHAR', 'INTEGER', 'DOUBLE'
    custom_field_types: dict = {
        'num_pixels': 'INTEGER',
        'QFLAG_value': 'INTEGER',
        'has_snow_presence': 'BOOLEAN',
        'has_iflags': 'BOOLEAN',                
    }
) -> List[dict]:
    """
    Builds L3 parameter schema for PhenoCams ROI data.

    This function generates a schema for Level 3 (L3) PhenoCams ROI parameters by leveraging the 
    internal helper function `__build_phenocams_rois_parameters_schema`. The generated schema is a list 
    of dictionaries, each containing information about a specific field required for storing PhenoCams ROI data.

    Parameters
    ----------
    station : Station
        An instance of the Station class containing phenocam ROIs.
    platform_id : str
        The identifier of the platform.
    platforms_type : str, optional
        The type of platform, by default 'PhenoCams'.
    prefix : str, optional
        A prefix to prepend to field names, by default 'L3'.
    parameters_dict : dict, optional
        A dictionary of parameters and their default values, by default:
        {
            'has_snow_presence': False,            
            'QFLAG_value': None,
            'QFLAG_weight': None,
            'num_pixels': None,
            'SUM_Red': None,
            'SUM_Green': None,
            'SUM_Blue': None,
            'MEAN_Red': None,
            'MEAN_Green': None,
            'MEAN_Blue': None,
            'SD_Red': None,
            'SD_Green': None,
            'SD_Blue': None,
            'MEANS_RGB_SUM': None,
            'GCC_daily_value': None,
            'RCC_daily_value': None
        }
    default_field_type : str, optional
        The default field type to use, by default 'DOUBLE'. 
        Options include 'BOOLEAN', 'VARCHAR', 'INTEGER', 'DOUBLE'.
    custom_field_types : dict, optional
        A dictionary to specify custom field types, by default:
        {
            'num_pixels': 'INTEGER',
            'QFLAG_value': 'INTEGER',
            'has_snow_presence': 'BOOLEAN',
            
        }

    Returns
    -------
    List[dict]
        A list of dictionaries where each dictionary represents a field with 'field_name', 'field_type', and 'field_default_value'.

    Examples
    --------
    >>> station = Station()  # Assume this is a properly initialized Station object
    >>> L3_schema = build_phenocams_rois_L3_parameters(
    ...     station=station,
    ...     platform_id='XYZ123',
    ...     prefix='L3',
    ...     parameters_dict={
    ...         'has_snow_presence': False,
    ...         'QFLAG_value': 0,
    ...         'QFLAG_weight': 1.0,
    ...         'num_pixels': 100,
    ...         'SUM_Red': 255,
    ...         'SUM_Green': 200,
    ...         'SUM_Blue': 150,
    ...         'MEAN_Red': 127.5,
    ...         'MEAN_Green': 100.0,
    ...         'MEAN_Blue': 75.0,
    ...         'SD_Red': 15.0,
    ...         'SD_Green': 10.0,
    ...         'SD_Blue': 5.0,
    ...         'MEANS_RGB_SUM': 450.0,
    ...         'GCC_daily_value': 0.45,
    ...         'RCC_daily_value': 0.35
    ...     },
    ...     default_field_type='DOUBLE',
    ...     custom_field_types={
    ...         'num_pixels': 'INTEGER',
    ...         'QFLAG_value': 'INTEGER',
    ...         'has_snow_presence': 'BOOLEAN',
    ...     }
    ... )
    >>> print(L3_schema)
    [{'field_name': 'L3_1_has_snow_presence', 'field_type': 'BOOLEAN', 'field_default_value': False}, ...]
    """
    return __build_phenocams_rois_parameters_schema(
        station=station,
        platform_id=platform_id,
        platforms_type=platforms_type,
        prefix=prefix,
        parameters_dict=parameters_dict,
        default_field_type=default_field_type,
        custom_field_types=custom_field_types,
    )



def get_schema_as_dict(platform_schema: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convert a list of schema dictionaries into a dictionary.

    Parameters
    ----------
    platform_schema : List[Dict[str, Any]]
        A list of dictionaries where each dictionary represents a schema field. 
        Each dictionary should contain the keys 'field_name' and 'field_default_value'.

    Returns
    -------
    Dict[str, Any]
        A dictionary where the keys are the 'field_name' values from the input list, 
        and the corresponding values are the 'field_default_value' from each dictionary.

    Examples
    --------
    >>> platform_schema = [
    ...     {'field_name': 'id', 'field_default_value': None},
    ...     {'field_name': 'name', 'field_default_value': ''},
    ...     {'field_name': 'age', 'field_default_value': 0}
    ... ]
    >>> get_schema_as_dict(platform_schema)
    {'id': None, 'name': '', 'age': 0}

    Notes
    -----
    This function assumes that each dictionary in the `platform_schema` list contains the keys
    'field_name' and 'field_default_value'. If these keys are missing, the function may raise
    a `KeyError`.

    Dependencies
    ------------
    - typing.List
    - typing.Dict
    - typing.Any
    """
    return {schema['field_name']: schema.get('field_default_value', None) for schema in platform_schema}
    
    
phenocams_core_schema = [
        {'field_name': 'catalog_guid',
     'field_type': 'VARCHAR',
     'field_default_value': None},
    {'field_name': 'year', 
     'field_type': 'INTEGER', 
     'field_default_value': None},
    {'field_name': 'creation_date',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'day_of_year',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'station_acronym',
    'field_type': 'VARCHAR',
    'field_default_value': None } ,
    {'field_name': 'location_id',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'platform_id',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'ecosystem_of_interest',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'platform_type',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'is_legacy',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'L0_name',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'is_L1',
     'field_type': 'BOOLEAN', 
     'field_default_value': False},
    {'field_name': 'is_ready_for_products_use',
    'field_type': 'BOOLEAN',
    'field_default_value': False},    
    {'field_name': 'catalog_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'origin_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_data_processing',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_code_sstc_core',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_platform_flags',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_qflag',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'version_schema_platform_phenocams',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'default_temporal_resolution',
    'field_type': 'BOOLEAN',
    'field_default_value': None},
    {'field_name': 'meantime_resolution',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'iflags_confirmed',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'has_snow_presence',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'sun_elevation_angle',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'sun_azimuth_angle',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'solar_elevation_class',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'QFLAG_image_value',
    'field_type': 'INTEGER',
    'field_default_value': None},
    {'field_name': 'QFLAG_image_weight',
    'field_type': 'DOUBLE',
    'field_default_value': None},
    {'field_name': 'is_per_image',
    'field_type': 'BOOLEAN',
    'field_default_value': False},    
    {'field_name': 'is_in_dataportal',
    'field_type': 'BOOLEAN',
    'field_default_value': False},
    {'field_name': 'fieldsites_filename',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'fieldsites_PID',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L1_QFI_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_RGB_CIMV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_GCC_CIMV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
    {'field_name': 'L2_RCC_CIMV_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},    
    {'field_name': 'L3_ROI_TS_filepath',
    'field_type': 'VARCHAR',
    'field_default_value': None},
] 



def build_phenocams_schema(
    station: Station, 
    platform_id: str, 
    phenocams_core_schema: List[Dict[str, Any]] = phenocams_core_schema
) -> List[Dict[str, Any]]:
    """
    Builds the complete schema for PhenoCams data by combining the core schema elements with 
    Phenocam Platforms Flags, Level 2 (L2) and Level 3 (L3) ROI parameters.

    This function generates the L2 and L3 ROI parameters for the given platform using the 
    `build_phenocams_rois_flags_schema`, `build_phenocams_rois_L2_parameters` and 
    `build_phenocams_rois_L3_parameters` functions. 
    It then appends these parameters to the provided PhenoCams core schema, resulting in a 
    comprehensive schema that covers all required fields.

    Parameters
    ----------
    station : Station
        An instance of the Station class containing phenocam ROIs.
    platform_id : str
        The identifier of the platform.
    phenocams_core_schema : List[Dict[str, Any]], optional
        The core schema for PhenoCams, provided as a list of dictionaries where each dictionary 
        represents a field. By default, this is set to the predefined `phenocams_core_schema`.

    Returns
    -------
    List[Dict[str, Any]]
        The complete schema for PhenoCams data, including core schema fields, L2, and L3 ROI parameters.

    Examples
    --------
    >>> station = Station()  # Assume this is a properly initialized Station object
    >>> complete_schema = build_phenocams_schema(
    ...     station=station,
    ...     platform_id='XYZ123'
    ... )
    >>> print(complete_schema)
    [{'field_name': 'catalog_guid', 'field_type': 'VARCHAR', 'field_default_value': None}, 
     {'field_name': 'ROI_01_flag_shadows', 'field_type': 'BOOLEAN', 'field_default_value': False},      
     {'field_name': 'L2_ROI_01_num_pixels', 'field_type': 'INTEGER', 'field_default_value': None}, 
     {'field_name': 'L3_ROI_01_has_snow_presence', 'field_type': 'BOOLEAN', 'field_default_value': False}, 
     ...]
    """
    
    phenocam_flags_dict = get_default_phenocam_flags(flags_yaml_filepath= config_flags_yaml_filepath)
    phenocams_rois_flags_schema = build_phenocams_rois_flags_schema(station=station, platform_id=platform_id, phenocam_flags_dict=phenocam_flags_dict)
    # Generate L2 and L3 ROI parameters
    phenocams_rois_L2_parameters = build_phenocams_rois_L2_parameters(station=station, platform_id=platform_id)
    phenocams_rois_L3_parameters = build_phenocams_rois_L3_parameters(station=station, platform_id=platform_id)
    
    # Append flags, L2 and L3 parameters to the core schema
    phenocams_core_schema += phenocams_rois_flags_schema
    phenocams_core_schema += phenocams_rois_L2_parameters
    phenocams_core_schema += phenocams_rois_L3_parameters
    
    # quickfix to avoid duplicated fields coming in
    in_dict = {}
    curated_schema = []
    for record in phenocams_core_schema:
        field_name = record['field_name'] 
        if field_name not in in_dict:
            in_dict[field_name] = {}
            curated_schema.append(record)
        
    
    
    return curated_schema
