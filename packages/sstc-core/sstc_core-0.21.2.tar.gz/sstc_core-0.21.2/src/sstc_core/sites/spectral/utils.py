import os
from datetime import datetime, timedelta
from PIL import Image
from PIL.ExifTags import TAGS
from shutil import copy2
from typing import Dict, Any, List
import unicodedata
import hashlib
import base64
import pytz
import re
import math
import numpy as np
import pandas as pd
from pysolar.solar import get_altitude, get_azimuth


def ensure_directory_exists(directory_path):
    """
    Ensure that a directory exists. If the directory (or any intermediate subdirectories)
    does not exist, it is created.

    Parameters:
    -----------
    directory_path : str
        The path to the directory that needs to be checked or created. This can include
        a full path to nested subdirectories.

    Returns:
    --------
    None

    Behavior:
    ---------
    - If the directory exists, nothing is done and a message is printed.
    - If the directory does not exist, it and any necessary intermediate directories
      are created, and a message is printed to confirm creation.

    Example usage:
    --------------
    directory = 'path/to/subdirectory'
    ensure_directory_exists(directory)
    
    Notes:
    ------
    - This function uses `os.makedirs()` to create directories, which will create 
      intermediate directories as needed, making it a recursive directory creation function.
    - If the directory already exists, no error is raised.
    """

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")


        

def copy_file_with_new_name(source_filepath, destination_directory, new_name)->str:
    """
    Copies a file from the source filepath to the destination directory with a new name while preserving the file format extension.

    Parameters:
        source_filepath (str): The path to the source file to be copied.
        destination_directory (str): The directory where the file should be copied to.
        new_name (str): The new name for the copied file (without extension).

    Returns:
        str: The path to the newly copied file.
    """
    # Extract the file extension from the source file
    file_extension = os.path.splitext(source_filepath)[1]

    # Create the full new file path
    new_file_path = os.path.join(destination_directory, f"{new_name}{file_extension}")

    # Ensure the destination directory exists
    os.makedirs(destination_directory, exist_ok=True)

    # Copy the file to the new location with the new name
    copy2(source_filepath, new_file_path)

    return str(new_file_path)



def generate_unique_id(data: dict, variable_names: list = ['formatted_date', 'station_acronym', 'location_id', 'platform_id']) -> str:
    """
    Generates a unique global identifier based on the provided variable names from the data dictionary.

    Parameters:
        data (dict): A dictionary containing the data fields.
        variable_names (list, optional): A list of variable names to include in the unique identifier. 
                                         Defaults to ['formatted_date', 'station_acronym', 'location_id', 'platform_id'].

    Returns:
        str: A short unique global identifier.
    """
    if variable_names is None:
        variable_names = ['formatted_date', 'station_acronym', 'location_id', 'platform_id']

    # Concatenate the specified fields from the data dictionary to form a unique string
    unique_string = "_".join(str(data[var]) for var in variable_names if var in data)
    
    # Generate the SHA-256 hash of the unique string
    hash_object = hashlib.sha256(unique_string.encode())
    hash_digest = hash_object.digest()
    
    # Take the first 12 bytes of the hash and encode them in Base64
    short_hash = base64.urlsafe_b64encode(hash_digest[:12]).decode('utf-8').rstrip('=')
    
    return short_hash


def day_of_year_to_month_day(year, day_of_year):
    # Calculate the date corresponding to the day of year
    date = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
    # Format the date as "MMM DD"
    return date.strftime('%b %d')

def extract_year(creation_date:str):
    """
    Extracts the year from the creation date.

    Parameters:
        creation_date (str): The creation date in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        int: The year extracted from the creation date.
    """
    date_obj = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
    return date_obj.year


def get_image_dates(filepath:str)->str:
    """
    Extracts the creation date from an image file's EXIF data.

    Parameters:
        filepath (str): The path to the image file.

    Returns:
        datetime: The creation date of the image if found, otherwise None.

    Raises:
        Exception: If an error occurs during the extraction process, it will print an error message.
    """
    try:
        image = Image.open(filepath)
        exif_data = image._getexif()

        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'DateTimeOriginal':
                    creation_date = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                    return creation_date
    except Exception as e:
        print(f"An error occurred with file {filepath}: {e}")
    return None


def list_image_files(dirpath:str, extensions:list = ['.jpg', '.jpeg']):
    """
    Lists all image files in a directory and its subdirectories with specified extensions.

    Parameters:
        dirpath (str): The root directory to search for image files.
        extensions (list): A list of file extensions to include in the search. Defaults to ['.jpg', '.JPEG', '.jpeg', '.JPG'].

    Returns:
        list: A list of file paths that match the specified extensions.
    """
    file_paths = []
    for root, _, files in os.walk(dirpath):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_paths.append(os.path.join(root, file))
    return file_paths


def group_images_by_date(filepaths: list):
    """
    Groups image files by their creation dates.

    This function takes a list of image file paths, extracts the creation date for each image,
    and groups the images by these dates. The grouped images are stored in a dictionary where 
    the keys are formatted creation dates and the values are lists of file paths that correspond
    to those dates.

    Parameters:
        filepaths (list): A list of file paths to the image files.

    Returns:
        dict: A dictionary where keys are formatted creation dates (as strings) and values are lists 
          of file paths that have those creation dates.

    Example:
        ```python    
        filepaths = ['/path/to/image1.jpg', '/path/to/image2.jpg']
        group_images_by_date(filepaths)
        {
            '2023-01-01 12:00:00': ['/path/to/image1.jpg'],
            '2023-01-02 13:00:00': ['/path/to/image2.jpg']
        }
        ```
    """
    date_dict = {}

    for filepath in filepaths:
        creation_date = get_image_dates(filepath)
        if creation_date:
            formatted_date = creation_date.strftime('%Y-%m-%d %H:%M:%S')
            if formatted_date not in date_dict:
                date_dict[formatted_date] = []
            date_dict[formatted_date].append(filepath)

    return date_dict


def filter_keys_with_multiple_files(image_date_dict:dict):
    """
    Filters and returns the keys from the image_date_dict that have multiple file paths.

    This function is used to detect duplicates by identifying keys (formatted creation dates)
    that have more than one file path associated with them in the provided dictionary.

    Parameters:
        image_date_dict (dict): A dictionary where keys are formatted creation dates (as strings) 
                            and values are lists of file paths that correspond to those dates.

    Returns:
        list: A list of keys (formatted creation dates) that have multiple file paths, indicating duplicates.

    Example:
        ```python
        image_date_dict = {
             '2023-01-01 12:00:00': ['/path/to/image1.jpg', '/path/to/image1_duplicate.jpg'],
             '2023-01-02 13:00:00': ['/path/to/image2.jpg']
        }
        filter_keys_with_multiple_files(image_date_dict)
        ['2023-01-01 12:00:00']
        ```
    """
    return [key for key, value in image_date_dict.items() if len(value) > 1]


def extract_two_dirs_and_filename(filepaths:list):
    """
    Extracts the last two subdirectories and the filename from a list of file paths.

    This function processes a list of file paths, extracts the last two subdirectories and 
    the filename from each path, and returns a dictionary where the keys are tuples 
    containing the two subdirectories and the filename (or fewer components if not enough 
    subdirectories are present), and the values are the full file paths.

    Parameters:
        filepaths (list): A list of file paths to process.

    Returns:
        dict: A dictionary where keys are tuples of (subdir_1, subdir_2, filename) or fewer
          components, and values are the corresponding full file paths.

    Example:
        ```python    
        filepaths = [
             '/path/to/subdir1/file1.jpg',
             '/another/path/to/subdir2/file2.jpg',
             '/file3.jpg'
         ]
        extract_two_dirs_and_filename(filepaths)
        {
            ('to', 'subdir1', 'file1.jpg'): '/path/to/subdir1/file1.jpg',
            ('to', 'subdir2', 'file2.jpg'): '/another/path/to/subdir2/file2.jpg',
            ('file3.jpg',): '/file3.jpg'
        }
        ```
    """
    extracted = {}
    for filepath in filepaths:
        parts = filepath.split(os.sep)
        if len(parts) >= 3:
            key = (parts[-3], parts[-2], parts[-1])
        elif len(parts) == 2:
            key = (parts[-2], parts[-1])
        elif len(parts) == 1:
            key = (parts[-1],)
        else:
            continue  # Skip empty or invalid file paths
        extracted[key] = filepath
    return extracted


def get_day_of_year(formatted_date: str) -> str:
    """
    Calculates the day of the year from a formatted date string and returns it as a string with leading zeros.

    Parameters:
        formatted_date (str): The date string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        str: The day of the year corresponding to the given date, formatted as a three-digit string with leading zeros.
    """
    date_obj = datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S')
    day_of_year = date_obj.timetuple().tm_yday
    return f"{day_of_year:03d}"


def phenocam_save_selected_images(filepaths_by_year_and_day: Dict[int, Dict[int, Dict[str, Dict[str, Any]]]], destination_dir: str):
    """
    Saves images with `is_selected` set to True to the specified destination directory.

    Parameters:
        filepaths_by_year_and_day (Dict[int, Dict[int, Dict[str, Dict[str, Any]]]]): Nested dictionary containing the data.
        destination_dir (str): The directory where the images will be saved.

    Returns:
        None
    """
    # Ensure the destination directory exists
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate through the data structure
    for year, days in filepaths_by_year_and_day.items():
        for day_of_year, records in days.items():
            for L0_name, data in records.items():
                if data.get('is_selected', False):
                    src_filepath = data['catalog_filepath']
                    if os.path.exists(src_filepath):
                        # Define the destination file path
                        filename = f"{L0_name}_{os.path.basename(src_filepath)}"
                        dest_filepath = os.path.join(destination_dir, filename)
                        
                        # Copy the file to the destination directory
                        copy2(src_filepath, dest_filepath)
                        print(f"Saved: {dest_filepath}")
                    else:
                        print(f"File not found: {src_filepath}")
                        
                        
def normalize_string(input_string: str) -> str:
    """
    Normalizes a string by converting it to lowercase and replacing accented or non-English
    characters with their corresponding English characters. Specially handles Nordic characters.

    Parameters:
        input_string (str): The string to normalize.

    Returns:
        str: The normalized string with all characters in lowercase and accented characters replaced.
    """
    # Decompose the unicode string into its components (base characters and diacritics)
    normalized = unicodedata.normalize('NFKD', input_string)

    # Encode the decomposed string into ASCII, ignoring non-ASCII characters (diacritics)
    ascii_bytes = normalized.encode('ASCII', 'ignore')

    # Decode the bytes back into a string
    ascii_string = ascii_bytes.decode('ASCII')

    # Convert to lowercase
    lower_string = ascii_string.lower()

    return lower_string


def is_within_time_window(formatted_date: str, start_time: str = "10:00:00", end_time: str = "14:30:00") -> bool:
    """
    Checks if the given date and time fall within the specified time window.

    Parameters:
        formatted_date (str): The date and time in the format '%Y-%m-%d %H:%M:%S'.
        start_time (str): The start of the time window in 'HH:MM:SS' format. Default is "10:00:00".
        end_time (str): The end of the time window in 'HH:MM:SS' format. Default is "14:30:00".

    Returns:
        bool: True if the time part of the formatted_date is within the time window, False otherwise.
    """
    # Convert the start and end times to time objects
    start_time_obj = datetime.strptime(start_time, '%H:%M:%S').time()
    end_time_obj = datetime.strptime(end_time, '%H:%M:%S').time()

    # Convert the formatted date to a datetime object and extract the time part
    date_obj = datetime.strptime(formatted_date, '%Y-%m-%d %H:%M:%S')
    creation_time = date_obj.time()

    # Check if the creation_time is within the time window
    return start_time_obj <= creation_time <= end_time_obj


def extract_keys_with_prefix(input_dict, starts_with='iflag_'):
    """
    Extracts keys from the input dictionary that start with the specified prefix.

    Parameters:
        input_dict (dict): The dictionary to filter.
        starts_with (str): The prefix to filter keys by. Default is 'iflag_'.

    Returns:
        dict: A new dictionary with only the keys starting with the specified prefix and their corresponding values.
    """
    return {key: value for key, value in input_dict.items() if key.startswith(starts_with)}




def set_all_values_to_false(input_dict:dict)->dict:
    """
    Sets all the values of the given dictionary to False.

    Parameters:
        input_dict (dict): The dictionary whose values will be set to False.

    Returns:
        dict: The dictionary with all values set to False.
    """
    return {key: False for key, value in input_dict.items()}

def have_values_changed(dict1, dict2):
    """
    Compares two dictionaries and returns a dictionary with the keys and new state
    values that have changed. Returns None if no values have changed.

    Parameters:
        dict1 (dict): The first dictionary representing the original state.
        dict2 (dict): The second dictionary representing the new state.

    Returns:
        dict or empty dict: A dictionary with changed keys and their new values, or and empty dict if no changes.
    """
    changed_values = {}

    # Iterate over the keys in the dictionaries and compare values
    for key in dict1:
        if key in dict2 and dict1[key] != dict2[key]:
            changed_values[key] = dict2[key]

    # Return the dictionary with changed values if any, otherwise return None
    return changed_values if changed_values else {}  


def get_month_day(day_of_year: int) -> str:
    """
    Convert a day of the year to a month and day string.

    Parameters:
        day_of_year (int): The day of the year.

    Returns:
        str: The corresponding month and day.
    """
    if not (1 <= int(day_of_year) <= 366):
        return "Invalid day of the year"

    start_of_year = datetime(year=2020, month=1, day=1)
    target_date = start_of_year + timedelta(days=int(day_of_year) - 1)
    return target_date.strftime("%B %d")



def calculate_sun_position(datetime_str:str, latitude_dd:float, longitude_dd:float, timezone_str='Europe/Stockholm')->Dict[str, float] :
    """
    Calculate the sun elevation and azimuth angles for a given datetime string, latitude, and longitude.

    Parameters:
        datetime_str (str): String representing the date and time in format 'YYYY-MM-DD HH:MM:SS'
        latitude_dd (float): Latitude in decimal degrees
        longitude_dd (float): Longitude in decimal degrees
        timezone_str (str): Timezone string, default is 'Europe/Stockholm' if None is provided
    Returns: 
        dict: Dictionary containing sun elevation angle and azimuth angle in degrees
    """
    # Parse the datetime string
    naive_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    
    # Use UTC if timezone_str is None
    if timezone_str is None:
        timezone_str = 'UTC'

    # Convert to a timezone-aware datetime
    local_tz = pytz.timezone(timezone_str)
    aware_datetime = local_tz.localize(naive_datetime)

    # Calculate the sun elevation angle
    sun_elevation_angle = get_altitude(latitude_dd, longitude_dd, aware_datetime)

    # Calculate the sun azimuth angle
    sun_azimuth_angle = get_azimuth(latitude_dd, longitude_dd, aware_datetime)

    return {'sun_elevation_angle': float(sun_elevation_angle), 'sun_azimuth_angle': float(sun_azimuth_angle)} 


def mean_datetime_str(datetime_list) -> str:
    """
    Calculate the mean datetime string from the max and min of the list.
    If the list has a single item, return that item.
    Handles cases where items may be either datetime objects or strings.
    Handles errors for invalid datetime strings and empty lists.

    Parameters:
    ----------
    datetime_list : list
        List of datetime objects or datetime strings in format 'YYYY-MM-DD HH:MM:SS'
    
    Returns:
    -------
    str
        Mean datetime string in format 'YYYY-MM-DD HH:MM:SS' or an error message
    
    Raises:
    ------
    ValueError
        If the list contains invalid datetime strings or the list is empty.
    
    Examples:
    --------
    >>> mean_datetime_str(["2023-08-20 12:00:00", "2023-08-21 12:00:00"])
    '2023-08-20 18:00:00'

    >>> mean_datetime_str([datetime(2023, 8, 20, 12, 0, 0), datetime(2023, 8, 21, 12, 0, 0)])
    '2023-08-20 18:00:00'
    """
    # Check if the list is empty
    if not datetime_list:
        return "Error: The datetime list is empty."

    try:
        # Convert all items to datetime objects if they are not already
        datetimes = []
        for dt in datetime_list:
            if isinstance(dt, str):
                datetimes.append(datetime.strptime(dt, '%Y-%m-%d %H:%M:%S'))
            elif isinstance(dt, datetime):
                datetimes.append(dt)
            else:
                return f"Error: Invalid item in datetime list: {dt}. Expected datetime object or string."

    except ValueError as e:
        return f"Error: Invalid datetime string format. {e}"

    # If the list has only one item, return that item as a string
    if len(datetimes) == 1:
        return datetimes[0].strftime('%Y-%m-%d %H:%M:%S')

    # Find the minimum and maximum datetimes
    min_datetime = min(datetimes)
    max_datetime = max(datetimes)

    # Calculate the mean datetime
    mean_datetime = min_datetime + (max_datetime - min_datetime) / 2

    # Convert the mean datetime back to string format
    mean_datetime_str = mean_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return mean_datetime_str


def get_solar_elevation_class(sun_elevation: float) -> int:
    """ 
    Categorize the solar elevation angles into 3 classes based on their values.
    The phenocam images are classified into three classes based on sun elevation angles:
    
    - Class 1: 0° - 20°
    - Class 2: 20° - 30°
    - Class 3: > 30°

    This scheme was adopted from the webcam network and image database for studying phenological changes in vegetation in Finland (Peltoniemi et al. 2018). The above class categories are coded as 1, 2, and 3 respectively. 
    Read more about this here: SITES Spectral - Data Quality Flagging (QFLAG) Documentation

    Parameters:
        sun_elevation (float): The sun elevation angle in degrees.

    Returns:
        int: The class category based on the sun elevation angle.
            - 1 for sun elevation angles between 0° and 20°.
            - 2 for sun elevation angles between 20° and 30°.
            - 3 for sun elevation angles greater than 30°.
    """
    
    if int(sun_elevation) < 20:
        solClass = 1
    elif 20 <= int(sun_elevation) <= 30:
        solClass = 2
    else:
        solClass = 3
        
    return solClass


def solar_illumination_conditions(
    latitude_dd: float,
    longitude_dd: float,
    record: dict,
    timezone_str: str = 'Europe/Stockholm'
) -> dict:
    """
    Calculates the solar illumination conditions for a given geolocation and record.

    This function calculates the sun's elevation and azimuth angles based on the creation date of a record, the latitude, 
    and the longitude of the location. It also classifies the solar elevation into a descriptive category.

    Parameters:
        latitude_dd (float): The latitude of the location in decimal degrees.
        longitude_dd (float): The longitude of the location in decimal degrees.
        record (dict): A dictionary containing metadata about the record. It must include the 'creation_date' key with a datetime string value.
        timezone_str (str, optional): The timezone string to use for the location (default is 'Europe/Stockholm').

    Returns:
        dict: A dictionary containing the following keys:
            - 'sun_elevation_angle' (float): The sun's elevation angle in degrees.
            - 'sun_azimuth_angle' (float): The sun's azimuth angle in degrees.
            - 'solar_elevation_class' (str): A classification of the solar elevation (e.g., 'Low', 'Medium', 'High').

    Example:
        ```python
        latitude_dd = 68.35
        longitude_dd = 18.82
        record = {
            'creation_date': '2024-06-07 08:17:23'
        }
        
        solar_conditions = solar_illumination_conditions(
            latitude_dd=latitude_dd,
            longitude_dd=longitude_dd,
            record=record,
            timezone_str='Europe/Stockholm'
        )
        
        print(solar_conditions)
        # Output might be: 
        # {'sun_elevation_angle': 45.2, 'sun_azimuth_angle': 120.5, 'solar_elevation_class': 'High'}
        ```

    Raises:
        KeyError: If the 'creation_date' key is missing from the record dictionary.
        ValueError: If there is an issue with calculating the solar position or classifying the solar elevation.

    Notes:
        - The `utils.calculate_sun_position` function is used to calculate the sun's position based on the datetime and location.
        - The `get_solar_elevation_class` function classifies the solar elevation angle into categories.

    Dependencies:
        - The function relies on the `utils.calculate_sun_position` and `get_solar_elevation_class` methods, which are assumed to be defined elsewhere in the codebase.
    """
    creation_date = record['creation_date']
     
    sun_position = calculate_sun_position(
        datetime_str=creation_date,
        latitude_dd=latitude_dd, 
        longitude_dd=longitude_dd, 
        timezone_str=timezone_str
    )
    
    sun_elevation_angle = sun_position.get('sun_elevation_angle', None)
    sun_azimuth_angle =  sun_position.get('sun_azimuth_angle', None)
    
    solar_elevation_class = get_solar_elevation_class(sun_elevation=sun_elevation_angle)
    
    return {
        'sun_elevation_angle': sun_elevation_angle,
        'sun_azimuth_angle': sun_azimuth_angle,
        'solar_elevation_class': solar_elevation_class
    }




def extract_keys_with_all_words(input_dict, words_list):
    """
    Extracts keys from the input dictionary where the associated string value contains all the words in the words_list,
    using regular expressions for matching.

    Parameters:
        input_dict (dict): The dictionary to filter.
        words_list (list): A list of words to search for in the string values.

    Returns:
        dict: A new dictionary with only the keys whose corresponding string values contain all the words in the words_list.
    """
    def contains_all_words(s, words):
        if not isinstance(s, str):
            return False
        return all(re.search(r'\b' + re.escape(word) + r'\b', s) for word in words)

    return {key: value for key, value in input_dict.items() if contains_all_words(value, words_list)}



def calculate_mean_time_resolution(records_list: list) -> dict:
    """
    Calculate the mean time resolution between records in a list of dictionaries.

    Parameters
    ----------
    records_list : list of dict
        List of dictionaries, each containing a 'creation_date' key.

    Returns
    -------
    meantime_resolution : dict
        A dictionary containing the mean time resolution between records with the keys:
        - 'hours': The average number of hours between records.
        - 'minutes': The average number of minutes between records.

    Examples
    --------
    >>> records_list = [
    >>>     {'creation_date': '2024-06-07 08:17:23'},
    >>>     {'creation_date': '2024-06-07 08:47:23'},
    >>>     {'creation_date': '2024-06-07 09:17:23'}
    >>> ]
    >>> calculate_mean_time_resolution(records_list)
    {'hours': 0, 'minutes': 30}
    """
    # Check if the records_list is too short to calculate a difference
    if len(records_list) <= 1:
        return {'hours': 0, 'minutes': 0}

    # Extract the creation dates and convert them to datetime objects
    creation_dates = sorted(
        [datetime.strptime(record['creation_date'], '%Y-%m-%d %H:%M:%S')
         for record in records_list]
    )

    # Calculate the time differences between consecutive dates
    time_diffs = np.diff(creation_dates)

    # Convert time differences to timedelta objects
    time_diffs = [diff if isinstance(diff, timedelta) else timedelta(seconds=diff.total_seconds()) for diff in time_diffs]

    # Calculate the mean time difference
    mean_diff = np.mean(time_diffs)

    # Check if mean_diff is NaN
    if isinstance(mean_diff, (np.float64, float)) and math.isnan(mean_diff):
        raise ValueError("Mean time difference calculation resulted in NaN. Check input records for valid dates.")

    # Ensure mean_diff is a timedelta object, not a numpy float
    if isinstance(mean_diff, (np.float64, float)):
        # Handle the case where mean_diff is a numpy float (number of seconds)
        mean_diff = timedelta(seconds=float(mean_diff))
    elif not isinstance(mean_diff, timedelta):
        raise ValueError("mean_diff is not a recognized type for time difference calculation.")

    # Convert mean_diff to a human-readable format
    total_seconds = mean_diff.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    # Create a dictionary to return the mean time resolution
    meantime_resolution = {'hours': int(hours), 'minutes': int(minutes)}

    return meantime_resolution


def select_dataframe_columns_by_strings(df: pd.DataFrame, substrings: list, exclude_columns: list) -> List[str]:
    """
    Select columns from a DataFrame whose names contain any of the specified substrings,
    with the option to exclude certain columns from the final selection.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame from which columns are to be selected.
        
    substrings : list
        A list of substrings. Columns containing any of these substrings in their names will be selected.
        
    exclude_columns : list
        A list of column names to exclude from the final selected columns.
    
    Returns:
    --------
    List[str]
        A list of column names that match the specified criteria.
    
    Description:
    ------------
    This function allows you to filter the columns of a pandas DataFrame based on the presence of
    one or more substrings in the column names. It then gives you the flexibility to exclude specific
    columns from the final selection if necessary.
    
    Notes:
    ------
    - If no columns match any of the substrings, the entire DataFrame's column list will be returned.
    - The function handles cases where multiple substrings match the same column by removing duplicates.
    - The function can also handle an empty `exclude_columns` list.
    
    """
    
    selected_columns = []
    
    # Iterate over the substring and filter columns containing any of them
    for substring in substrings:
        selected_columns.extend([col for col in df.columns if substring in col]) 
    
    # Remove duplicates in case a column matches multiple substrings
    selected_columns = list(set(selected_columns))
    
    # If no columns were found, return the entire DataFrame
    if not selected_columns:
        selected_columns = df.columns.tolist()
        
    # Handle exclusion of columns
    if exclude_columns:
        selected_columns = [col for col in selected_columns if col not in exclude_columns]
        
    # Return the DataFrame with selected columns
    return df[sorted(selected_columns)]
    