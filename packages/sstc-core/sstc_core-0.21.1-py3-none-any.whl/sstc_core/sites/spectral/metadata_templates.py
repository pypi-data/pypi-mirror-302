import os

def update_metadata_from_dict(metadata_dict, new_filename, destination_dir):
    """
    Creates a metadata file based on the provided dictionary of metadata values and saves it
    to the specified destination directory. Additionally, a subdirectory with the same name
    as the metadata file (excluding the file extension) is created in the destination directory.

    Parameters:
    ----------
    metadata_dict : dict
        A dictionary containing the metadata key-value pairs. The keys should match the metadata
        field names (e.g., 'TITLE', 'TIME PERIOD', 'DESCRIPTION', etc.). If a key is missing,
        the function will use a default value based on a predefined template.

    new_filename : str
        The name of the new metadata file to be created, including the file extension (e.g., 'metadata.txt').

    destination_dir : str
        The path to the directory where the new metadata file and subdirectory should be saved.
        If the directory does not exist, it will be created.

    Returns:
    -------
    str or None
        The full path to the newly created metadata file if the operation is successful.
        If an error occurs during the process, the function returns None.

    Example:
    -------
    metadata_dict = {
        'TITLE': 'Updated Phenocamera RGB image collection from Abisko Observatory',
        'TIME PERIOD': '2022-05-01 08:00:00 - 2022-12-31 18:00:00',
        'TIME RESOLUTION': 'HOURLY',
        'PROCESSING METHODS': 'Basic color correction applied',
        'DESCRIPTION': 'Updated collection of images with enhanced processing.',
    }

    new_filename = 'updated_metadata.txt'
    destination_dir = 'path_to_destination_directory'

    new_file_path = update_metadata_from_dict(metadata_dict, new_filename, destination_dir)

    if new_file_path:
        print(f"The file was successfully created at: {new_file_path}")
    else:
        print("Failed to create the metadata file.")
    """
    try:
        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Extract the filename without extension to create the subdirectory
        subdirectory_name = os.path.splitext(new_filename)[0]
        subdirectory_path = os.path.join(destination_dir, subdirectory_name)

        # Create the subdirectory
        if not os.path.exists(subdirectory_path):
            os.makedirs(subdirectory_path)

        # Define the metadata structure based on the template
        metadata_template = (
            f"TITLE: {metadata_dict.get('TITLE', 'Phenocamera RGB image collection from Abisko Observatory, north-western Sweden.')}\n"
            f"SITES STATION: {metadata_dict.get('SITES STATION', 'Abisko Scientific Research Station')}\n"
            f"TIME PERIOD: {metadata_dict.get('TIME PERIOD', '2021-04-01 10:00:00 - 2021-11-30 14:00:00')}\n"
            f"TIME RESOLUTION: {metadata_dict.get('TIME RESOLUTION', 'BIHOURLY')}\n"
            f"TIME ZONE: {metadata_dict.get('TIME ZONE', 'UTC +1')}\n"
            f"SAMPLING POINT: {metadata_dict.get('SAMPLING POINT', 'Abisko Scientific Research Station, Mast 4.5m Phenocam 01')}\n"
            f"LATITUDE: {metadata_dict.get('LATITUDE', '68.353921')}\n"
            f"LONGITUDE: {metadata_dict.get('LONGITUDE', '18.789888')}\n"
            f"ALTITUDE: {metadata_dict.get('ALTITUDE', '381 m a.s.l.')}\n"
            f"\n"
            f"FILE RETRIEVED FROM: {metadata_dict.get('FILE RETRIEVED FROM', 'https://data.fieldsites.se Link to metadata landing page is available in separate file in the downloaded zip.')}\n"
            f"DATA POLICY: {metadata_dict.get('DATA POLICY', 'SITES data is licensed under a Creative Commons Attribution 4.0 international license (http://creativecommons.org/licenses/by/4.0/).')}\n"
            f"\n"
            f"PARAMETERS & UNITS: {metadata_dict.get('PARAMETERS & UNITS', 'Digital Numbers (DN)')}\n"
            f"\n"
            f"DESCRIPTION: {metadata_dict.get('DESCRIPTION', 'Collection of quality filtered phenocamera RGB images every 2 hours from 10 a.m. to 2 p.m. The phenocamera pointed to Mount Nuolja. The ecosystems in the images are subalpine birch forest (Betula pubescens var. czerepan) and alpine shrubland (mainly Salix spp., Empetrum nigrum, and Vaccinium vitis–idaea) in the upper slope of Mount Nuolja.')}\n"
            f"\n"
            f"SENSOR DESCRIPTION: {metadata_dict.get('SENSOR DESCRIPTION', 'Data acquired with Nikon D300s RGB phenology camera, with wide field of view (FOV) angle of 60 degrees. Images stored in JPG format.')}\n"
            f"\n"
            f"DATA ACQUISITION: {metadata_dict.get('DATA ACQUISITION', 'The original photos were acquired with phenology camera mounted on the rooftop of the observation house, at a height of 4.5 m above ground, looking west (270 degrees) and an off-nadir angle of 59 degrees. The phenocamera acquired images from 10 a.m. to 2 p.m. every two hours. The phenocamera operates between April and November. The area surveyed by the phenocamera projects a footprint on the ground, the centroid of which is approximately defined by the following coordinate (latitude, longitude in GCS WGS84, decimal degrees): 68.353921, 18.789888.')}\n"
            f"\n"
            f"PROCESSING METHODS: {metadata_dict.get('PROCESSING METHODS', 'No image processing applied at this stage. However, low quality images were filtered out manually from the original image collection. Low quality refers to images that contain sun glare, rain droplets, fog, or shadows, or represent low-light or blurry conditions.')}\n"
            f"DATA PRODUCT TYPE: {metadata_dict.get('DATA PRODUCT TYPE', 'L1_QFI')}\n"
            f"DATA PRODUCT DESCRIPTION: {metadata_dict.get('DATA PRODUCT DESCRIPTION', 'Data Processing Level 1 Quality Filtered Images')}\n"
            
        )

        # Define the full path for the new metadata file in the destination directory
        new_file_path = os.path.join(destination_dir, new_filename)

        # Write the constructed metadata to the new file
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(metadata_template)

        print(f"Metadata file has been saved to: {new_file_path}")
        print(f"Subdirectory created at: {subdirectory_path}")

        # Return the path of the newly created metadata file
        return new_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
