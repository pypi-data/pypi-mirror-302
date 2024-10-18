import cv2
import numpy as np


def convert_to_bool(value):
    """
    Converts a value to a boolean type. This function handles different types of boolean-like values
    and ensures that the output is a standard Python boolean (`True` or `False`).

    Parameters:
        value (Any): The input value to be converted to a boolean. This can include various types
                     such as numpy boolean types, Python boolean types, or other values.

    Returns:
        bool: The converted boolean value. If the input value is a boolean type (numpy or Python),
              it returns the corresponding boolean value. For any other input, it returns `False`.

    Examples:
        ```python
        >>> convert_to_bool(np.bool_(True))
        True

        >>> convert_to_bool(True)
        True

        >>> convert_to_bool(False)
        False

        >>> convert_to_bool(1)
        False

        >>> convert_to_bool("string")
        False
        ```
    """
    if isinstance(value, (np.bool_, bool)):
        return bool(value)
    return False


def detect_blur(image, method='laplacian', threshold=100):
    """
    Detect if an image is blurry using specified metrics.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        method (str): The method used for blurriness detection. Options are 'laplacian' and 'sobel'.
        threshold (float): The threshold value for blurriness detection. If the computed metric is below this threshold, the image is considered blurry.

    Returns:
        bool: True if the image is detected as blurry, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)

        # Detect blur using Laplacian method
        is_blurry = detect_blur(image, method='laplacian', threshold=100)
        print(f"Laplacian method - Is image blurry? {is_blurry}")

        # Detect blur using Sobel method
        is_blurry_sobel = detect_blur(image, method='sobel', threshold=10)
        print(f"Sobel method - Is image blurry? {is_blurry_sobel}")        
        
        ```
    """
    if not isinstance(image, np.ndarray):
        raise ValueError("Input image must be a numpy ndarray.")
    if method not in ['laplacian', 'sobel']:
        raise ValueError("Invalid method. Choose 'laplacian' or 'sobel'.")
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if method == 'laplacian':
        # Compute the Laplacian variance as the measure of blurriness
        blur_value = cv2.Laplacian(gray, cv2.CV_64F).var()
    elif method == 'sobel':
        # Compute the Sobel gradient magnitude as the measure of blurriness
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_mag = np.sqrt(sobelx**2 + sobely**2)
        blur_value = np.mean(sobel_mag)
    
    # Determine if the image is blurry based on the threshold
    return convert_to_bool(blur_value < threshold)


def detect_snow(image, brightness_threshold=200, saturation_threshold=50):
    """
    Detect snow in an image based on brightness and saturation thresholds.
    
    Snowflakes often appear as bright white spots with varying sizes. A simple approach 
    is to identify regions in the image with high brightness and low saturation.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        brightness_threshold (int): The minimum brightness value to consider as snow.
        saturation_threshold (int): The maximum saturation value to consider as snow.

    Returns:
        bool: True if snow is detected, False otherwise.
        
    Example:
        ```python
            image_path = 'image.jpg'
            image = cv2.imread(image_path)
            if detect_snow(image):
                print("Snow detected")
            else:
                print("No snow detected")
        ```
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = hsv[:, :, 2]
    saturation = hsv[:, :, 1]

    snow_mask = (brightness > brightness_threshold) & (saturation < saturation_threshold)
    snow_percentage = np.sum(snow_mask) / (image.shape[0] * image.shape[1])

    return convert_to_bool(snow_percentage > 0.01)  # Adjust percentage threshold as needed


def detect_rain(image, min_line_length=100, max_line_gap=10):
    """
    Detect rain in an image using line detection.
    
    Rain can be detected by analyzing the vertical streaks or lines in an image. This can be achieved
    using edge detection and line detection techniques.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_line_length (int): Minimum line length to be considered as rain.
        max_line_gap (int): Maximum gap between line segments to be considered as a single line.

    Returns:
        bool: True if rain is detected, False otherwise.
        
    Example:
        ```python
            image_path = 'image.jpg'
            image = cv2.imread(image_path)
            if detect_rain(image):
                print("Rain detected")
            else:
                print("No rain detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=min_line_length, maxLineGap=max_line_gap)
    
    if lines is not None:
        return True
    return False


def detect_water_drops(image, min_radius=5, max_radius=20):
    """
    Detect water drops on the lens using circular Hough Transform.
    
    Water drops on the lens create localized distortions. 
    Detecting them involves looking for circular regions with different 
    textures or colors.
    

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_radius (int): Minimum radius of water drops to detect.
        max_radius (int): Maximum radius of water drops to detect.

    Returns:
        bool: True if water drops are detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_water_drops(image):
            print("Water drops detected")
        else:
            print("No water drops detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=100, param2=30, minRadius=min_radius, maxRadius=max_radius)
    
    if circles is not None:
        return True
    return False

def detect_dirt(image, min_area=500, max_area=2000):
    """
    Detect dirt on the lens using blob detection.
    
    Dirt on the lens often creates localized dark spots or blobs. 
    This can be detected using blob detection techniques.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_area (int): Minimum area of the dirt blobs to detect.
        max_area (int): Maximum area of the dirt blobs to detect.

    Returns:
        bool: True if dirt is detected, False otherwise.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    
    for stat in stats[1:]:  # Skip the first component as it's the background
        area = stat[cv2.CC_STAT_AREA]
        if min_area < area < max_area:
            return True
    return False


def detect_obstructions(image, min_contour_area=10000):
    """
    Detect obstructions in the image using contour detection to find large objects.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        min_contour_area (int): Minimum contour area to be considered as an obstruction.

    Returns:
        bool: True if obstructions are detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_obstructions(image):
            print("Obstruction detected")
        else:
            print("No obstruction detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_contour_area:
            return True
    return False


def assess_brightness(image, dark_threshold=50, bright_threshold=200):
    """
    Assess the brightness of an image and return a status code.
    
    Assessing brightness involves calculating the average intensity of the image and checking it 
    against thresholds for too dark or too bright conditions.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        dark_threshold (int): The brightness value below which the image is considered too dark.
        bright_threshold (int): The brightness value above which the image is considered too bright.

    Returns:
        int: 0 if brightness is optimal, -1 if very dark, 1 if very bright.
    
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        brightness_status = assess_brightness(image)
        
        if brightness_status == -1:
            print("Very dark image")
        elif brightness_status == 1:
            print("Very bright image")
        else:
            print("Optimal brightness")        
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    average_brightness = np.mean(gray)

    if average_brightness < dark_threshold:
        return 1  # Very dark image
    elif average_brightness > bright_threshold:
        return 1  # Very bright image
    else:
        return 0  # Optimal brightness
    
    
def detect_glare(image, threshold=240):
    """
    Detect glare in an image based on pixel value thresholds.
    
    Detecting glare involves identifying overexposed areas in the image, 
    usually found in bright regions.


    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        threshold (int): The pixel value threshold above which pixels are considered to have glare.

    Returns:
        bool: True if glare is detected, False otherwise.
    
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_glare(image):
            print("Glare detected")
        else:
            print("No glare detected")        
        ```
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    _, _, v = cv2.split(hsv)
    glare_mask = v > threshold
    glare_percentage = np.sum(glare_mask) / (image.shape[0] * image.shape[1])

    return convert_to_bool(glare_percentage > 0.01)  # Adjust percentage threshold as needed


def detect_fog(image, threshold=0.5):
    """
    Detect fog in an image by analyzing edge detection.
    
    Detecting fog involves analyzing the contrast in the image, as fog often reduces contrast.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        threshold (float): The ratio of edge pixels to total pixels below which the image is considered foggy.

    Returns:
        bool: True if fog is detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_fog(image):
            print("Fog detected")
        else:
            print("No fog detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = np.sum(edges > 0) / (image.shape[0] * image.shape[1])

    return convert_to_bool(edge_ratio < threshold)

def detect_high_quality(image_path):
    """
    Detects if image is high quality. Not yet implemented.

    Parameters:
        image_path (str): Path to the image file.

    Returns:
        bool: False.
        
    Raises:
        ValueError: if Image not found or path is incorrect.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or path is incorrect")
    
    return False  # Adjust range as needed


def detect_haze(image_path, threshold=120):
    """
    Detects haze in an image based on a brightness threshold.

    Parameters:
        image_path (str): Path to the image file.
        threshold (int): Threshold value to classify haze. Default is 120.

    Returns:
        bool: True if haze is detected, False otherwise.
    
    Raises:
        ValueError: if Image not found or path is incorrect.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or path is incorrect")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_image)
    return convert_to_bool( threshold < avg_brightness < 150 )  # Adjust range as needed

def detect_clouds(image_path, threshold=200):
    """
    Detects clouds in an image based on a brightness threshold.

    Parameters:
        image_path (str): Path to the image file.
        threshold (int): Threshold value to classify clouds. Default is 200.

    Returns:
        bool: True if clouds are detected, False otherwise.
    
    Raises:
        ValueError: if Image not found or path is incorrect.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or path is incorrect")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_image)
    return convert_to_bool( avg_brightness > threshold )

def detect_shadows(image_path, threshold=50):
    """
    Detects shadows in an image based on a brightness threshold.

    Parameters:
        image_path (str): Path to the image file.
        threshold (int): Threshold value to classify shadows. Default is 50.

    Returns:
        bool: True if shadows are detected, False otherwise.
    
    Raises:
        ValueError: if Image not found or path is incorrect.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or path is incorrect")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_image)
    return convert_to_bool( avg_brightness < threshold )

def detect_ice(image_path, threshold=220):
    """
    Detects ice in an image based on a brightness threshold.

    Parameters:
        image_path (str): Path to the image file.
        threshold (int): Threshold value to classify ice. Default is 220.

    Returns:
        bool: True if ice is detected, False otherwise.
    
    Raises:
        ValueError: if Image not found or path is incorrect.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or path is incorrect")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray_image)
    return convert_to_bool( avg_brightness > threshold )


def detect_rotation(image, angle_threshold=10):
    """
    Detect if an image has been rotated by analyzing the orientation of lines.

    Parameters:
        image (numpy.ndarray): The input image in BGR format.
        angle_threshold (float): The angle threshold above which the image is considered rotated.

    Returns:
        bool: True if significant rotation is detected, False otherwise.
        
    Example:
        ```python
        image_path = 'image.jpg'
        image = cv2.imread(image_path)
        if detect_rotation(image):
            print("Image rotation detected")
        else:
            print("No significant image rotation detected")
        ```
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta)
            angle = (angle - 90) % 180  # Normalize angle
            angles.append(angle)

        average_angle = np.mean(angles)
        return convert_to_bool(abs(average_angle) > angle_threshold)

    return False
