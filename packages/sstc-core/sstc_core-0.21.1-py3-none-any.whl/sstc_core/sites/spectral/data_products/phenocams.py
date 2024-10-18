import os
from pathlib import Path
from typing import List, Dict, Any, Union
import numpy as np
import pandas as pd
import cv2
from PIL import Image
from sstc_core.sites.spectral.io_tools import load_yaml
from sstc_core.sites.spectral import utils
from sstc_core.sites.spectral.data_products.qflags import compute_qflag

# Get the absolute path of the current script
__script_parent_path = os.path.dirname(os.path.abspath(__file__))
config_flags_yaml_filepath = os.path.join( os.path.dirname(__script_parent_path), 'config', 'phenocam_flags.yaml')


if not os.path.exists(config_flags_yaml_filepath):
    raise FileExistsError(f'{config_flags_yaml_filepath}')

def serialize_polygons(phenocam_rois):
    """
    Converts a dictionary of polygons to be YAML-friendly by converting tuples to lists.
    
    Parameters:
        phenocam_rois (dict of dict): Dictionary where keys are ROI names and values are dictionaries representing polygons.
    
    Returns:
        yaml_friendly_rois (dict of dict): Dictionary with tuples converted to lists.
    """
    yaml_friendly_rois = {}
    for roi, polygon in phenocam_rois.items():
        yaml_friendly_polygon = {
            'points': [list(point) for point in polygon['points']],
            'color': list(polygon['color']),
            'thickness': polygon['thickness']
        }
        yaml_friendly_rois[roi] = yaml_friendly_polygon
    return yaml_friendly_rois

def deserialize_polygons(yaml_friendly_rois):
    """
    Converts YAML-friendly polygons back to their original format with tuples.
    
    Parameters:
        yaml_friendly_rois (dict of dict): Dictionary where keys are ROI names and values are dictionaries representing polygons in YAML-friendly format.
    
    Returns:
        original_rois (dict of dict): Dictionary with points and color as tuples.
    """
    original_rois = {}
    for roi, polygon in yaml_friendly_rois.items():
        original_polygon = {
            'points': [tuple(point) for point in polygon['points']],
            'color': tuple(polygon['color']),
            'thickness': polygon['thickness']
        }
        original_rois[roi] = original_polygon
    return original_rois


def overlay_polygons(image_path, phenocam_rois: dict, show_names: bool = True, font_scale: float = 1.0):
    """
    Overlays polygons on an image and optionally labels them with their respective ROI names.

    Parameters:
        image_path (str): Path to the image file.
        phenocam_rois (dict): Dictionary where keys are ROI names and values are dictionaries representing polygons.
        Each dictionary should have the following keys:
        - 'points' (list of tuple): List of (x, y) tuples representing the vertices of the polygon.
        - 'color' (tuple): (B, G, R) color of the polygon border.
        - 'thickness' (int): Thickness of the polygon border.
        show_names (bool): Whether to display the ROI names on the image. Default is True.
        font_scale (float): Scale factor for the font size of the ROI names. Default is 1.0.

    Returns:
        numpy.ndarray: The image with polygons overlaid, in RGB format.
    """
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("Image not found or path is incorrect")
    
    for roi, polygon in phenocam_rois.items():
        # Extract points, color, and thickness from the polygon dictionary
        points = np.array(polygon['points'], dtype=np.int32)
        color = polygon['color']
        thickness = polygon['thickness']
        
        # Draw the polygon on the image
        cv2.polylines(img, [points], isClosed=True, color=color, thickness=thickness)
        
        if show_names:
            # Calculate the centroid of the polygon for labeling
            M = cv2.moments(points)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
            else:
                # In case of a degenerate polygon where area is zero
                cX, cY = points[0][0], points[0][1]
            
            # Overlay the ROI name at the centroid of the polygon
            cv2.putText(img, roi, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, 2, cv2.LINE_AA)

    # Convert the image from BGR to RGB before returning
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img_rgb

def compute_RGB_daily_average(records_list: List[Dict[str, Any]], products_dirpath: str, datatype_acronym: str = 'RGB', product_processing_level: str = 'L2_daily') -> Path:
    """
    Computes daily average RGB images from a list of records and saves them as .jpg files.

    Parameters:
        records_list (List[Dict[str, Any]]): List of dictionaries where each dictionary contains metadata and the image path.
        products_dirpath (str): Path to the directory where the processed images will be saved.
        datatype_acronym (str, optional): Acronym for the data type, default is 'RGB'.
        product_processing_level (str, optional): Processing level for the product, default is 'L2_daily'.

    Returns:
        Path: Path to the directory where the daily averaged images are saved.
    """
    images = []
    daily_image_catalog_guids = []

    for record in records_list:
        try:
            catalog_guid = record['catalog_guid']
            year = record['year']
            day_of_year = record['day_of_year']
            station_acronym = record['station_acronym']
            location_id = record['location_id']
            platform_id = record['platform_id']
            catalog_filepath = record['catalog_filepath']
            
            product_id = f'L2_{datatype_acronym}_CIMV'

            output_dirpath = Path(products_dirpath) / product_id / str(year)

            if not os.path.exists(output_dirpath):
                os.makedirs(output_dirpath)

            img = cv2.imread(catalog_filepath)
            if img is not None:
                images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                daily_image_catalog_guids.append(catalog_guid)
            else:
                print(f"Warning: Unable to read image at {catalog_filepath}")
        except KeyError as e:
            print(f"Error: Missing key {e} in record {record}")
        except Exception as e:
            print(f"Unexpected error processing record {record}: {e}")

    if images:
        try:
            # Compute element-wise daily average
            avgImg = np.mean(images, axis=0)
            
            # Converting float64 type ndarray to uint8
            intImage = np.around(avgImg).astype(np.uint8)  # Round first and then convert to integer
            
            # Saving the daily average as image
            im = Image.fromarray(intImage)
            
            product_name = f'SITES-{product_id}-{station_acronym}-{location_id}-{platform_id}-{year}-DOY_{day_of_year}_{product_processing_level}.JPG'
            output_filepath = output_dirpath / product_name

            # Save image in the defined path
            im.save(output_filepath)
            print(f"Saved daily averaged image to {output_filepath}")
        except Exception as e:
            print(f"Error during image processing or saving: {e}")
    else:
        print("No images were processed. No output file created.")

    return str(output_filepath)


def compute_GCC_RCC(daily_rgb_filepath: str, products_dirpath: str, year: int) -> dict:
    """
    Computes GCC and RCC images from a daily average RGB image and saves them as grayscale images.

    Parameters:
        daily_rgb_filepath (str): File path to the daily average RGB image.
        products_dirpath (str): Path to the directory where the processed images will be saved.
        year (int): Year for which the GCC and RCC images are being processed.

    Returns:
        dict: Dictionary containing file paths to the saved GCC and RCC images.
    """
    try:
        # Define directories to save GCC and RCC images
        gcc_dirpath = Path(products_dirpath) / 'L2_GCC_CIMV'  / str(year)
        rcc_dirpath = Path(products_dirpath) / 'L2_RCC_CIMV' / str(year)
        
        # Ensure the directories exist
        gcc_dirpath.mkdir(parents=True, exist_ok=True)
        rcc_dirpath.mkdir(parents=True, exist_ok=True)
        
        # Extracting image file name
        imgName = os.path.basename(daily_rgb_filepath)
        
        # Reading the RGB image
        cv_img = cv2.imread(daily_rgb_filepath)
        if cv_img is None:
            raise FileNotFoundError(f"Image file not found or unable to read: {daily_rgb_filepath}")
        
        # Extracting RGB bands as separate numpy arrays
        B = cv_img[:,:,0]
        G = cv_img[:,:,1]
        R = cv_img[:,:,2]

        # Element-wise addition of BGR array to calculate Total DN values in RGB band (i.e. R+G+B)
        DNtotal = cv_img.sum(axis=2)

        # Compute pixel-wise GCC and RCC from daily average images
        gcc = np.divide(G, DNtotal, out=np.zeros_like(G, dtype=float), where=DNtotal!=0)
        rcc = np.divide(R, DNtotal, out=np.zeros_like(R, dtype=float), where=DNtotal!=0)

        # Convert NaN to zero
        gcc = np.nan_to_num(gcc, copy=False)
        rcc = np.nan_to_num(rcc, copy=False)

        # Converting GCC and RCC to smoothly range from 0 - 255 as 'uint8' data type from 'float64'
        intImage1 = (gcc * 255).astype(np.uint8) 
        intImage2 = (rcc * 255).astype(np.uint8)

        # Convert to BGR format for saving
        cv_img_gcc = cv2.cvtColor(intImage1, cv2.COLOR_GRAY2BGR)
        cv_img_rcc = cv2.cvtColor(intImage2, cv2.COLOR_GRAY2BGR)

        # Define paths for saving images with given file names
        gcc_filepath = os.path.join(gcc_dirpath, imgName.replace('RGB', 'GCC'))
        rcc_filepath = os.path.join(rcc_dirpath, imgName.replace('RGB', 'RCC'))

        # Save images in the defined paths
        cv2.imwrite(gcc_filepath, cv_img_gcc)
        cv2.imwrite(rcc_filepath, cv_img_rcc)
        
        return {'gcc_filepath': str(gcc_filepath), 'rcc_filepath': str(rcc_filepath)}

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Missing key {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}
    
    
    
def rois_mask_and_sum(image_path: str, phenocam_rois: dict) -> dict:
    """
    Masks an image based on the provided ROIs, calculates the sum of pixel values inside each ROI for R, G, and B channels,
    and returns a dictionary with the ROI name, sum of pixel values for each channel, and the number of summed pixels.

    Parameters:
        image_path (str): Path to the image file.
        phenocam_rois (dict): Dictionary where keys are ROI names and values are dictionaries representing polygons.
        Each dictionary should have the following keys:
        - 'points' (list of tuple): List of (x, y) tuples representing the vertices of the polygon.
        - 'color' (tuple): (B, G, R) color of the polygon border.
        - 'thickness' (int): Thickness of the polygon border.

    Returns:
        dict: A dictionary where each key is an ROI name, and the value is another dictionary containing:
              - 'sum_r': The sum of all pixel values inside the ROI mask for the red channel.
              - 'sum_g': The sum of all pixel values inside the ROI mask for the green channel.
              - 'sum_b': The sum of all pixel values inside the ROI mask for the blue channel.
              - 'num_pixels': The number of pixels that were summed inside the ROI.
              
    Example:
        ```python
        # Example usage
        if __name__ == "__main__":
            # Define the phenocam ROIs
            phenocam_rois = {
                'ROI_01': {
                    'points': [(100, 1800), (2700, 1550), (2500, 2700), (100, 2700)],
                    'color': (0, 255, 0),
                    'thickness': 7
                },
                'ROI_02': {
                    'points': [(100, 930), (3700, 1050), (3700, 1200), (100, 1400)],
                    'color': (0, 0, 255),
                    'thickness': 7
                },
                'ROI_03': {
                    'points': [(750, 600), (3700, 650), (3500, 950), (100, 830)],
                    'color': (255, 0, 0),
                    'thickness': 7
                }
            }
            
            # Apply the function to an image
            image_path = "path/to/your/image.jpg"
            roi_sums = rois_mask_and_sum(image_path, phenocam_rois)
        
        # >>>
                {
            'ROI_01': {
                'sum_r': 123456789,
                'sum_g': 987654321,
                'sum_b': 567890123,
                'num_pixels': 2553501
            },
            'ROI_02': {
                'sum_r': 112233445,
                'sum_g': 556677889,
                'sum_b': 223344556,
                'num_pixels': 1120071
            },
            'ROI_03': {
                'sum_r': 998877665,
                'sum_g': 554433221,
                'sum_b': 776655443,
                'num_pixels': 881151
            }
        }        
        ```
    """
    # Read the image as a color image (BGR format)
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("Image not found or path is incorrect")
    
    roi_sums = {}

    for roi, polygon in phenocam_rois.items():
        # Create a mask for the ROI
        mask = np.zeros(img.shape[:2], dtype=np.uint8)  # Mask with the same height and width as the image
        points = np.array(polygon['points'], dtype=np.int32)
        cv2.fillPoly(mask, [points], 255)
        
        # Apply the mask to each channel
        masked_img = cv2.bitwise_and(img, img, mask=mask)
        
        # Calculate the sum of pixel values within the ROI for each channel
        sum_b = np.sum(masked_img[:, :, 0][mask == 255])
        sum_g = np.sum(masked_img[:, :, 1][mask == 255])
        sum_r = np.sum(masked_img[:, :, 2][mask == 255])
        num_pixels = np.sum(mask == 255)
        
        # Store the results in the dictionary
        roi_sums[roi] = {
            'SUM_Red': int(sum_r),
            'SUM_Green': int(sum_g),
            'SUM_Blue': int(sum_b),
            'num_pixels': int(num_pixels)
        }

    return roi_sums    

def convert_rois_sums_to_single_dict(rois_sums_dict):
    """
    Converts the rois_sums_dict into a single dictionary with keys in the format 'L2_<ROI_NAME>_<suffix>'.

    The `rois_sums_dict` is expected to contain sums of pixel values for each color channel (R, G, B) and the number of pixels
    within each ROI, as calculated by the `rois_mask_and_sum` function.

    Parameters:
        rois_sums_dict (dict): A dictionary where keys are ROI names and values are dictionaries containing:
                               - 'sum_r': The sum of all pixel values inside the ROI mask for the red channel.
                               - 'sum_g': The sum of all pixel values inside the ROI mask for the green channel.
                               - 'sum_b': The sum of all pixel values inside the ROI mask for the blue channel.
                               - 'num_pixels': The number of pixels that were summed inside the ROI.

    Returns:
        dict: A single dictionary containing the combined key-value pairs in the format:
              - 'L2_<ROI_NAME>_sum_r': Sum of pixel values for the red channel in the ROI.
              - 'L2_<ROI_NAME>_sum_g': Sum of pixel values for the green channel in the ROI.
              - 'L2_<ROI_NAME>_sum_b': Sum of pixel values for the blue channel in the ROI.
              - 'L2_<ROI_NAME>_num_pixels': Number of pixels summed in the ROI.
              
    Example:
        ```python
        
        rois_sums_dict = {
            'ROI_01': {
                'sum_r': 123456789,
                'sum_g': 987654321,
                'sum_b': 567890123,
                'num_pixels': 2553501
            },
            'ROI_02': {
                'sum_r': 112233445,
                'sum_g': 556677889,
                'sum_b': 223344556,
                'num_pixels': 1120071
            },
            'ROI_03': {
                'sum_r': 998877665,
                'sum_g': 554433221,
                'sum_b': 776655443,
                'num_pixels': 881151
            }
        }

        # Create a single dictionary
        single_dict = convert_rois_sums_to_single_dict(rois_sums_dict)

        print(single_dict)
                
        # Output:
        
            {
            'L2_ROI_01_sum_r': 123456789,
            'L2_ROI_01_sum_g': 987654321,
            'L2_ROI_01_sum_b': 567890123,
            'L2_ROI_01_num_pixels': 2553501,
            'L2_ROI_02_sum_r': 112233445,
            'L2_ROI_02_sum_g': 556677889,
            'L2_ROI_02_sum_b': 223344556,
            'L2_ROI_02_num_pixels': 1120071,
            'L2_ROI_03_sum_r': 998877665,
            'L2_ROI_03_sum_g': 554433221,
            'L2_ROI_03_sum_b': 776655443,
            'L2_ROI_03_num_pixels': 881151
        }
        ```
    """
    # Initialize an empty dictionary
    combined_dict = {}

    # Iterate over the rois_sums_dict to create the single dictionary
    for roi_name, metrics in rois_sums_dict.items():
        for suffix, value in metrics.items():
            combined_dict[f'L2_{roi_name}_{suffix}'] = value

    return combined_dict


def group_records_by_unique_filepath(input_dict: dict, filepath_key: str) -> dict:
    """
    Groups records by unique file paths specified by a given key.

    This function iterates over a dictionary of records, identifies unique values based on the specified 
    file path key, and groups the record identifiers (keys) that share the same file path.

    Parameters:
        input_dict (dict): A dictionary where each key is a unique identifier and each value is a dictionary 
                           containing various fields, including the specified file path.
        filepath_key (str): The key used to access the file path in the nested dictionaries.

    Returns:
        dict: A dictionary where the keys are unique file paths, and the values are lists of record identifiers 
              (keys from the input dictionary) that share the same file path.

    Example:
        ```python
        input_dict = {
            'cV_HhjIV0vpTmqh0': {'L2_RGB_CIMV_filepath': '/path/to/file1.jpg'},
            'd4kTg4oRZdSk9kbV': {'L2_RGB_CIMV_filepath': '/path/to/file1.jpg'},
            'zpl4JHxP79ef-Az6': {'L2_RGB_CIMV_filepath': '/path/to/file2.jpg'}
        }
        unique_values = group_records_by_unique_filepath(input_dict, 'L2_RGB_CIMV_filepath')
        # Result:
        # {
        #   '/path/to/file1.jpg': ['cV_HhjIV0vpTmqh0', 'd4kTg4oRZdSk9kbV'],
        #   '/path/to/file2.jpg': ['zpl4JHxP79ef-Az6']
        # }
        ```

    Raises:
        KeyError: If the filepath_key is not found in one of the dictionaries in input_dict.
    """

    unique_values = {}

    for record_id, value_dict in input_dict.items():
        try:
            value = value_dict[filepath_key]
        except KeyError:
            raise KeyError(f"The key '{filepath_key}' was not found in the record with ID '{record_id}'.")

        if value not in unique_values:
            unique_values[value] = []

        unique_values[value].append(record_id)

    return unique_values


def get_default_phenocam_flags(flags_yaml_filepath: str ) -> dict:
    """
    Load and return the default PhenoCam flags from a YAML configuration file.

    This function reads a YAML file containing default flag settings for PhenoCam data processing and returns the contents as a dictionary. These flags are typically used to control various aspects of image quality assessment, such as detecting snow, glare, or other artifacts.

    Parameters
    ----------
    flags_yaml_filepath : str, optional
        The file path to the YAML configuration file containing the PhenoCam flags. 
        Expected config file:  '/config/phenocam_flags.yaml'.

    Returns
    -------
    dict
        A dictionary containing the default PhenoCam flags as specified in the YAML configuration file.

    Raises
    ------
    FileNotFoundError
        If the YAML file specified by `flags_yaml_filepath` does not exist.
    yaml.YAMLError
        If there is an error parsing the YAML file.

    Examples
    --------
    >>> flags = get_default_phenocam_flags(flags_yaml_filepath)
    >>> print(flags)
    {
        'flag_brightness': False,
        'flag_blur': False,
        'flag_snow': True,
        ...
    }

    Notes
    -----
    The function relies on a YAML file for configuration. Ensure that the file path is correct and that the YAML file is properly formatted.

    Dependencies
    ------------
    - yaml (PyYAML library): For loading YAML files.
    - load_yaml (function): A utility function used to load the YAML file into a dictionary.
    """
    flags_dict = load_yaml(filepath=flags_yaml_filepath)

    return flags_dict


def load_iflags_penalties(flags_yaml_filepath: str) -> dict:
    """
    Load penalties for PhenoCam individual flags from a YAML configuration file.

    This function retrieves the default PhenoCam flags using the `get_default_phenocam_flags` function and then extracts the associated penalties for each flag. If a penalty is not specified for a flag, it defaults to 0.

    Parameters
    ----------
    flags_yaml_filepath : str, optional
        The file path to the YAML configuration file containing the PhenoCam flags. 
        Expected config file:  '/config/phenocam_flags.yaml'.


    Returns
    -------
    dict
        A dictionary where the keys are the flag names and the values are the penalities associated with each individual flag. 
        If a penalty is not provided for a flag in the YAML configuration, a default penalty of 1 is assigned.

    Examples
    --------
    >>> penalties = load_iflags_penalties()
    >>> print(penalties)
    {
        'flag_brightness': 0.8,
        'flag_blur': 0.9,
        'flag_snow': 1.0,
        ...
    }

    Notes
    -----
    The function assumes that the penaöties for the PhenoCam flags are defined in the YAML configuration file loaded by 
    the `get_default_phenocam_flags` function. If no penalty value is defined for a particular flag, a default penalty of 0 is used.

    Dependencies
    ------------
    - `get_default_phenocam_flags` (function): This function is used to load the default PhenoCam flags from a YAML file.
    - yaml (PyYAML library): Used for loading YAML files if needed by the `get_default_phenocam_flags` function.
    """
    flags = get_default_phenocam_flags(flags_yaml_filepath = flags_yaml_filepath)
    iflags_penalties_dict ={}
    for flag in flags:
        iflags_penalties_dict[flag] = flags[flag].get('penalty_value', 0)

    return iflags_penalties_dict


def calculate_final_weights_for_rois(record: dict, rois_list: list, iflags_penalties_dict: dict) -> dict:
    """
    Calculate the final weights to be applied for each ROI in a valid record.

    Parameters
    ----------
        - record (dict): The record containing the ROI data.
        - rois_list (list): List of ROI names to process.
        - iflags_penalties_dict (dict): Dictionary containing flags and_penalties values.

    Returns
    -------
        - dict: Dictionary containing the final weights for each ROI.
    """
    
    
    final_weights = {}

    for roi in rois_list:
        total_iflag_penality_value = 0
        iflag_disable_for_processing = record[f'{roi}_iflag_disable_for_processing'] 
        if not iflag_disable_for_processing:
                
            # Iterate over all flags for the ROI and sum their weights if the flag is True
            for flag, data in iflags_penalties_dict.items():
                flag_key = f"{roi}_{flag}"
                if record.get(flag_key, False):
                    total_iflag_penality_value += data.get('penalty_value', 0)

            # Calculate the final weight
            final_weight = 1 - total_iflag_penality_value

            # If the final weight is less than 0, set it to 0
            if final_weight < 0:
                final_weight = 0
            elif final_weight >1:
                final_weight = 1        
        else:
            final_weight = 0
            
        final_weights[roi] = final_weight

    return final_weights


def calculate_mean_datetime(records: List[Dict[str, Union[str, int, float]]]) -> str:
    """
    Calculate the mean datetime from a list of records.

    Parameters
    ----------
    records : List[Dict[str, Union[str, int, float]]]
        A list of records, where each record is a dictionary containing a 'creation_date' key with its value as a string.

    Returns
    -------
    str
        A string representing the mean datetime calculated from the 'creation_date' values in the input records.

    Notes
    -----
    This function extracts the 'creation_date' from each record, computes the mean datetime using the utility function
    `utils.mean_datetime_str`, and returns the result as a string.
    """
    
    
    datetime_list = [item['creation_date'] for item in records]
    return utils.mean_datetime_str(datetime_list=datetime_list)


def compute_qflag_for_day(
    records: List[Dict], 
    latitude: float, 
    longitude: float,
    default_temporal_resolution: bool,
    is_per_image: bool
    ) -> Union[float, None]:
    
    """
    Compute the quality flag (Q-flag) for a given day based on the provided records, location, and configuration parameters.

    Parameters
    ----------
    records : List[Dict]
        A list of records where each record is a dictionary containing various metadata, including a unique 'catalog_guid'.
    latitude : float
        The latitude of the location for which the Q-flag is to be computed, in decimal degrees.
    longitude : float
        The longitude of the location for which the Q-flag is to be computed, in decimal degrees.
    default_temporal_resolution : bool
        If True, uses the default temporal resolution for processing; if False, uses a custom temporal resolution.
    is_per_image : bool
        If True, computes the Q-flag for each image individually; if False, computes a single Q-flag for the day.

    Returns
    -------
    Union[float, None]
        The computed Q-flag as a float if successful, or None if the Q-flag could not be computed.

    Notes
    -----
    This function consolidates the records into a dictionary indexed by 'catalog_guid', then calls `compute_qflag`
    to calculate the Q-flag for the day based on the provided location and settings.
    """
    records_dict = {record['catalog_guid']: record for record in records}
    return compute_qflag(
        latitude_dd=latitude,
        longitude_dd=longitude,
        records_dict=records_dict,
        timezone_str='Europe/Stockholm',
        is_per_image=is_per_image,
        default_temporal_resolution=default_temporal_resolution,
    )
    

def process_records_for_roi(
    records: List[Dict],
    rois_list: list, 
    roi: str, 
    iflags_penalties_dict: Dict[str, float], 
    overwrite_weight: bool, 
    skip_iflags_list = [
                'iflag_sunny', 
                'iflag_cloudy',
                'iflag_full_overcast', 
                'iflag_initial_green_up',
                'iflag_initial_peek_greeness',
                'iflag_initial_lead_discoloration',
                'iflag_initial_leaf_fall', 
                ],
    ) -> Dict[str, Union[float, bool, int, Dict]]:
    """
    Processes a list of records for a specific Region of Interest (ROI) to calculate weighted means, standard deviations, and other metrics.

    This method processes all records corresponding to a given ROI. It calculates weighted mean values for the red, green, and blue channels, 
    along with their respective standard deviations. The method also computes the sum of weights, GCC (Green Chromatic Coordinates) value, 
    RCC (Red Chromatic Coordinates) value, and additional metadata.

    Parameters
    ----------
    records : List[Dict]
        A list of records where each record is a dictionary containing various data fields including the ROI values.
    roi : str
        The name of the Region of Interest (ROI) to be processed (e.g., 'ROI_01', 'ROI_02').
    iflags_penalties_dict : Dict[str, float]
        A dictionary containing penalties (as weight modifiers) for various flags associated with the ROI. The keys are flag names, and the values are penalty weights.
    overwrite_weight : bool
        If True, the weight for each record is set to 1, ignoring the calculated final weights from the penalties. If False, the calculated weight is used.
    skip_iflags_list : List[str], optional
        A list of flags to skip when checking for the presence of flags in the ROI (default is ['iflag_sunny', 'iflag_cloudy', 'iflag_full_overcast']).

    Returns
    -------
    Dict[str, Union[float, bool, int, Dict]]
        A dictionary containing the following keys:
            - 'weighted_mean_red': Weighted mean of the red channel for the ROI.
            - 'weighted_mean_green': Weighted mean of the green channel for the ROI.
            - 'weighted_mean_blue': Weighted mean of the blue channel for the ROI.
            - 'sum_of_weights': The sum of weights used in the calculation.
            - 'sum_of_weighted_means': The sum of the weighted means for red, green, and blue channels.
            - 'GCC_value': Green Chromatic Coordinates value for the ROI.
            - 'RCC_value': Red Chromatic Coordinates value for the ROI.
            - 'total_pixels': Total number of pixels considered in the ROI.
            - 'std_red': Standard deviation of the red channel values.
            - 'std_green': Standard deviation of the green channel values.
            - 'std_blue': Standard deviation of the blue channel values.
            - 'weights_used': A dictionary mapping each `catalog_guid` to a dictionary containing 'weight' and 'roi' keys.
            - 'num_valid_records': The number of valid records processed for the ROI.
            - 'has_iflags': Boolean indicating if any flags (excluding those in `skip_iflags_list`) were set for the ROI.
            - 'has_snow_presence': Boolean indicating if snow presence was detected in the ROI.

    Notes
    -----
    - The standard deviations ('std_red', 'std_green', 'std_blue') are calculated only if there is more than one valid record.
    - The method skips any records where the ROI has `iflag_disable_for_processing` set to True.
    - The `calculate_final_weights_for_rois` function is used to determine the final weight for each record unless `overwrite_weight` is True.

    Example
    -------
    ```python
    roi_results = process_records_for_roi(
        records=my_records,
        roi='ROI_01',
        iflags_penalties_dict={'flag_haze': 0.5, 'flag_clouds': 0.25},
        overwrite_weight=False
    )
    ```
    """   
   
    roi_results = {
        "weighted_mean_red": 0, "weighted_mean_green": 0, "weighted_mean_blue": 0, 
        "sum_of_weights": 0, "GCC_value": 0, "RCC_value": 0, "total_pixels": 0, 
        "std_red": 0, "std_green": 0, "std_blue": 0, "weights_used": {}, 
        "num_valid_records": 0, "has_iflags": False, 'has_snow_presence': False,
        'iflag_disable_for_processing': False, 'overwrite_weight': overwrite_weight,
    }
    
    red_values, green_values, blue_values = [], [], []
    red_weighted_sum, green_weighted_sum, blue_weighted_sum = 0, 0, 0
    total_weight = 0
    
    for record in records:
        disable_for_processing = record[f'{roi}_iflag_disable_for_processing'] 
        if not disable_for_processing: 
                
            weight = 1 if overwrite_weight else calculate_final_weights_for_rois(record, rois_list, iflags_penalties_dict).get(roi, 1)
            num_pixels = record.get(f"L2_{roi}_num_pixels", 0)
            if num_pixels > 0:
                red_mean = record.get(f"L2_{roi}_SUM_Red", 0) / num_pixels
                green_mean = record.get(f"L2_{roi}_SUM_Green", 0) / num_pixels
                blue_mean = record.get(f"L2_{roi}_SUM_Blue", 0) / num_pixels

                # Accumulate weighted sums and weights for final weighted average calculation
                red_weighted_sum += red_mean * weight
                green_weighted_sum += green_mean * weight
                blue_weighted_sum += blue_mean * weight
                total_weight += weight

                roi_results["total_pixels"] += num_pixels
                roi_results["weights_used"][record["catalog_guid"]] = {"weight": weight, "roi": roi}
                roi_results["num_valid_records"] += 1
                roi_results['has_iflags'] = any([v for k, v in utils.extract_keys_with_prefix(input_dict=record, starts_with=roi).items() if k not in skip_iflags_list])
                roi_results['has_snow_presence'] = record[f'L3_{roi}_has_snow_presence']                
                
                red_values.append(red_mean)
                green_values.append(green_mean)
                blue_values.append(blue_mean)              
            

    if total_weight > 0:
        # Final weighted mean calculation
        roi_results["weighted_mean_red"] = red_weighted_sum / total_weight
        roi_results["weighted_mean_green"] = green_weighted_sum / total_weight
        roi_results["weighted_mean_blue"] = blue_weighted_sum / total_weight

        roi_results["sum_of_weights"] = total_weight
        roi_results["sum_of_weighted_means"] = roi_results["weighted_mean_red"] + roi_results["weighted_mean_green"] + roi_results["weighted_mean_blue"]
        
        if roi_results["sum_of_weighted_means"] > 0:
            roi_results["GCC_value"] = roi_results["weighted_mean_green"] / roi_results["sum_of_weighted_means"]
            roi_results["RCC_value"] = roi_results["weighted_mean_red"] / roi_results["sum_of_weighted_means"]

        if len(red_values) > 1:
            roi_results["std_red"] = float(np.std(red_values))
            roi_results["std_green"] = float(np.std(green_values))
            roi_results["std_blue"] = float(np.std(blue_values))
                        
    return roi_results



def calculate_roi_weighted_means_and_stds(
    doy_dict_with_records_list: Dict[int, List[Dict[str, Union[int, float, bool, str]]]], 
    rois_list: List[str], 
    iflags_penalties_dict: Dict[str, float],
    latitude_dd: float, 
    longitude_dd: float,
    overwrite_weight: bool = True,
    skip_iflags_list = [
                'iflag_sunny', 
                'iflag_cloudy',
                'iflag_full_overcast', 
                'iflag_initial_green_up',
                'iflag_initial_peek_greeness',
                'iflag_initial_lead_discoloration',
                'iflag_initial_leaf_fall', 
                ]
) -> Dict[int, Dict[str, Union[float, Dict]]]:
    """    
    Calculate the weighted means, standard deviations, and derived records (GCC, RCC) per day of year for each ROI.

    
    Parameters
    ----------    
    doy_dict_with_records_list : dict
        A dictionary where each key is a day of the year and the corresponding value is a list of records for that day. Each record contains pixel data and other relevant information.
    rois_list : list
        A list of strings representing the names of Regions of Interest (ROIs) to process.
    iflags_penalties_dict : dict
        A dictionary mapping flag values to their corresponding penalty values, used to adjust the calculations based on the presence of flags in the data.
    latitude_dd : float
        The latitude in decimal degrees, used to calculate the quality flag (QFLAG) for the records.
    longitude_dd : float
        The longitude in decimal degrees, used in conjunction with latitude to calculate the QFLAG for the records.
    overwrite_weight : bool, optional
        If True, the weight is set to 1 for all records, regardless of the calculated value. Defaults to True.

    Returns
    -------
    dict
        A dictionary where each key is a day of the year, and the corresponding value is a nested dictionary containing the calculated metrics for each ROI.
    """
    
    #################
    results = {}
    
    for day_of_year, records in doy_dict_with_records_list.items():
        mean_datetime = calculate_mean_datetime(records)
        
        r_list = [{'creation_date': record['creation_date']} for record in records]
        
        meantime_resolution = utils.calculate_mean_time_resolution(records_list=records)
        
        default_temporal_resolution = False if meantime_resolution['hours'] > 0 or meantime_resolution['minutes'] > 30 else True 
        
        qflag_dict = compute_qflag_for_day(
            records, 
            latitude_dd,
            longitude_dd, 
            default_temporal_resolution=default_temporal_resolution,
            is_per_image=False)
        
        day_xtras = {
            'mean_datetime': mean_datetime, 
            'QFLAG_value': qflag_dict['QFLAG'] , 
            'meantime_resolution':  f"{str(meantime_resolution["hours"]).zfill(2)}:{str(meantime_resolution["hours"]).zfill(2)}",
            'default_temporal_resolution': default_temporal_resolution, 
            }
         
            
        #day_xtras_per_roi ={ roi:{**day_xtras} for roi in rois_list}
        #TODO: fill process_records_for_rois with all parameters 
        
        day_results = {roi: {**process_records_for_roi(
            records=records,  
            rois_list=rois_list,
            roi=roi, 
            iflags_penalties_dict= iflags_penalties_dict,
            overwrite_weight=overwrite_weight,
            skip_iflags_list = skip_iflags_list,
            )} for roi in rois_list}
        
        
        results[day_of_year] =  day_results  #{**day_results, **day_xtras_per_roi}  
    
    return results



def calculate_roi_weighted_means_and_stds_per_record(
    doy_dict_with_records_list: Dict[int, List[Dict[str, Any]]],
    rois_list: List[str],
    iflags_penalties_dict: Dict[str, Any],
    overwrite_weight: bool = True
) -> Dict[int, Dict[str, Dict[str, Any]]]:
    """
    Calculate the weighted means for each Region of Interest (ROI) for each valid record grouped by day of year.

    Parameters
    ----------
    doy_dict_with_records_list : dict
        Dictionary where the key is the day of the year (int) and the value is a list of records (each record being a dictionary).
    rois_list : list
        List of ROI names to process (strings).
    iflags_penalties_dict : dict
        Dictionary containing flags and penalties values that influence the weights for each ROI.
    overwrite_weight : bool, optional
        If True, sets the weight to 1 for all records, overriding any calculated weight. Defaults to True.

    Returns
    -------
    dict
        A dictionary where each key is a day of the year (int) and the value is another dictionary that maps
        record GUIDs to their corresponding ROI data, which includes weighted means for red, green, and blue values,
        the total number of pixels, and the weight.
    """
    results = {}

    for day_of_year, records in doy_dict_with_records_list.items():
        day_results = {}

        for record in records:
            record_guid = record["catalog_guid"]
            # disable_for_processing = record['disable_for_processing'] 
            record_results = {
                roi: {
                    "weighted_mean_red": None,
                    "weighted_mean_green": None,
                    "weighted_mean_blue": None,
                    "weight": 1,
                    "total_pixels": None,
                    # We do not need the disable flag here as this is calculated by the image based. 
                    # Better use the `is_ready_for_products_use` so here we commented the line
                    # 'iflag_disable_for_processing': record[f'{roi}_iflag_disable_for_processing'] 
                } for roi in rois_list
            }

            # Calculate final weights for each ROI using the provided flags and penalties dictionary
            final_weights = calculate_final_weights_for_rois(record, rois_list, iflags_penalties_dict)

            for roi, weight in final_weights.items():
                # Override weight if overwrite_weight flag is set
                weight = 1 if overwrite_weight else weight

                if weight > 0:
                    num_pixels = record.get(f"L2_{roi}_num_pixels", 0)
                    if num_pixels > 0:
                        red_mean = record.get(f"L2_{roi}_SUM_Red", 0) / num_pixels
                        green_mean = record.get(f"L2_{roi}_SUM_Green", 0) / num_pixels
                        blue_mean = record.get(f"L2_{roi}_SUM_Blue", 0) / num_pixels

                        # Calculate the weighted means correctly
                        record_results[roi]["weighted_mean_red"] = red_mean * weight
                        record_results[roi]["weighted_mean_green"] = green_mean * weight
                        record_results[roi]["weighted_mean_blue"] = blue_mean * weight
                        record_results[roi]["total_pixels"] = num_pixels
                        record_results[roi]["weight"] = weight
                    else:
                        # Set values to zero if there are no pixels
                        record_results[roi]["weighted_mean_red"] = 0
                        record_results[roi]["weighted_mean_green"] = 0
                        record_results[roi]["weighted_mean_blue"] = 0
                        record_results[roi]["total_pixels"] = 0
                        record_results[roi]["weight"] = 0

            day_results[record_guid] = record_results

        results[day_of_year] = day_results

    return results


def create_l2_parameters_dataframe(data_dict, year):
    """
    Creates a DataFrame indexed by day of the year for a given `year`, containing all parameter values 
    for each ROI, using the catalog_guid to help form the column names.
    
    Parameters
    ----------
    data_dict : dict
        Dictionary containing the data indexed by day of year, catalog_guid, and ROI name.
    year : int
        The year for which the DataFrame is being created (used to calculate days in the year).
        
    Returns
    -------
    pd.DataFrame
        DataFrame with days of the year as the index and columns representing the parameter
        values for each ROI, with catalog_guid included in the column names.
    """
    # Determine the number of days in the year (considering leap years)
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    
    # Initialize an empty dictionary to store data
    data = {day: {} for day in range(1, days_in_year + 1)}
    
    # Iterate through the data dictionary
    for day, catalogs in data_dict.items():
        day = int(day)
        for catalog_guid, rois in catalogs.items():
            for roi_name, parameters in rois.items():
                for param_name, param_value in parameters.items():
                    # Form the column name based on catalog_guid, ROI, and parameter
                    column_name = f"{catalog_guid}__{roi_name}_{param_name}"
                    # Store the parameter value in the data dictionary
                    data[day][column_name] = param_value
    
    # Create a DataFrame from the dictionary
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Sort the DataFrame by the index (days of the year)
    df.sort_index(inplace=True)
    
    # Fill missing values with None
    df = df.reindex(range(1, days_in_year + 1)).fillna(pd.NA)
    
    return df


def create_l3_parameters_dataframe(data_dict, year):
    """
    Creates a DataFrame indexed by day of the year for a given `year`, containing all parameter values 
    for each ROI, using `L3_{roi_name}_{param_name}` to form the column names. The `weights_used` entries
    are expanded to form columns in the format `L3_{roi_name}_weight__{catalog_guid}`.
    
    Parameters
    ----------
    data_dict : dict
        Dictionary containing the data indexed by day of year and ROI name.
    year : int
        The year for which the DataFrame is being created (used to calculate days in the year).
        
    Returns
    -------
    pd.DataFrame
        DataFrame with days of the year as the index and columns representing the parameter
        values for each ROI, including expanded `weights_used`.
    """
    # Determine the number of days in the year (considering leap years)
    days_in_year = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    
    # Initialize an empty dictionary to store data
    data = {day: {} for day in range(1, days_in_year + 1)}
    
    # Iterate through the data dictionary
    for day, rois in data_dict.items():
        day = int(day)
        for roi_name, parameters in rois.items():
            for param_name, param_value in parameters.items():
                if param_name == "weights_used" and isinstance(param_value, dict):
                    # NOTE: Leave this as pass so it will not be included in the dataframe
                    pass
                    # Handle the weights_used separately
                    #for catalog_guid, weight_info in param_value.items():
                         
                        # weight_column_name = f"L3_{roi_name}_weight__{catalog_guid}"
                        #data[day][weight_column_name] = weight_info.get('weight')
                #elif 'QFLAG' in param_name:
                #    QFLAG = param_value['QFLAG']
                #    column_name = f"L3_{roi_name}_{'QFLAG_value'}"
                #    data[day][column_name] = QFLAG
                      
                    
                # else:
                #----------------------
                ## HERE CHANGED v0.19.1 commented
                #if 'weighted' in param_name:
                #    param_name = param_name.replace('weighted_', '')
                #------------------------------
                # Form the column name based on ROI and parameter
                column_name = f"L3_{roi_name}_{param_name}"
                # Store the parameter value in the data dictionary
                data[day][column_name] = param_value

    # Create a DataFrame from the dictionary
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Sort the DataFrame by the index (days of the year)
    df.sort_index(inplace=True)
    
    # Fill missing values with pd.NA (a proper placeholder for missing data)
    df = df.reindex(range(1, days_in_year + 1)).fillna(pd.NA)
    
    return df


