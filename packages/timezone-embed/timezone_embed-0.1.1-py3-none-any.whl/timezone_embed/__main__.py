import subprocess
import json
import argparse
import glob
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import re
import os

# Path to exiftool binary
EXIFTOOL_PATH = "exiftool"

# Function to convert DMS (degrees, minutes, seconds) to decimal degrees
def dms_to_decimal(dms_str):
    # Parse the DMS string (example: "56 deg 39' 15.55\" N" or "4 deg 54' 23.59\" W")
    dms_pattern = r"(\d+) deg (\d+)' ([\d\.]+)\" ([NSEW])"
    match = re.match(dms_pattern, dms_str)
    
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")
    
    degrees = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))
    direction = match.group(4)
    
    # Convert to decimal degrees
    decimal_degrees = degrees + (minutes / 60) + (seconds / 3600)
    
    # If the direction is South or West, make the value negative
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

# Function to get GPS data from an image
def get_gps_data(image_path):
    # Extract EXIF data
    result = subprocess.run([EXIFTOOL_PATH, "-GPSLatitude", "-GPSLongitude", "-j", image_path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        raise Exception(f"Error reading EXIF data: {result.stderr.decode()}")
    
    exif_data = json.loads(result.stdout.decode())
    
    if not exif_data or 'GPSLatitude' not in exif_data[0] or 'GPSLongitude' not in exif_data[0]:
        raise ValueError(f"No GPS data found in {image_path}")
    
    latitude_dms = exif_data[0]['GPSLatitude']
    longitude_dms = exif_data[0]['GPSLongitude']
    
    # Convert DMS to decimal
    latitude = dms_to_decimal(latitude_dms)
    longitude = dms_to_decimal(longitude_dms)
    
    return latitude, longitude

# Function to get timezone based on GPS coordinates
def get_timezone_from_gps(latitude, longitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
    
    if not timezone_str:
        raise ValueError("Could not determine timezone for the given GPS coordinates.")
    
    return timezone_str

# Function to apply timezone to EXIF DateTimeOriginal and store the offset in OffsetTimeOriginal
def apply_timezone(image_path, timezone_str):
    # Get the current DateTimeOriginal
    result = subprocess.run([EXIFTOOL_PATH, "-DateTimeOriginal", "-j", image_path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        raise Exception(f"Error reading EXIF DateTimeOriginal: {result.stderr.decode()}")
    
    exif_data = json.loads(result.stdout.decode())
    if not exif_data or 'DateTimeOriginal' not in exif_data[0]:
        raise ValueError(f"No DateTimeOriginal found in {image_path}")
    
    original_datetime_str = exif_data[0]['DateTimeOriginal']
    original_datetime = datetime.strptime(original_datetime_str, "%Y:%m:%d %H:%M:%S")
    
    # Apply timezone
    timezone = pytz.timezone(timezone_str)
    localized_datetime = timezone.localize(original_datetime)
    
    # Extract the timezone offset in the format (+HH:MM or -HH:MM)
    offset = localized_datetime.strftime("%z")
    offset_formatted = f"{offset[:3]}:{offset[3:]}"  # Format as +HH:MM
    
    # Update EXIF OffsetTimeOriginal with the timezone offset
    subprocess.run([EXIFTOOL_PATH, f"-OffsetTime*={offset_formatted}", "-overwrite_original", image_path],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print(f"Updated {image_path} with timezone offset: {offset_formatted}")

# Function to process a single image
def process_image(image_path):
    try:
        # Step 1: Get GPS data
        latitude, longitude = get_gps_data(image_path)
        print(f"GPS coordinates for {image_path}: {latitude}, {longitude}")
        
        # Step 2: Get timezone from GPS coordinates
        timezone_str = get_timezone_from_gps(latitude, longitude)
        print(f"Timezone for {image_path}: {timezone_str}")
        
        # Step 3: Apply timezone to DateTimeOriginal and store the offset in OffsetTimeOriginal
        apply_timezone(image_path, timezone_str)
        print(f"Timezone offset updated for {image_path}!")
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Main function to handle multiple images
def update_images_timezone(image_paths):
    for image_path in image_paths:
        process_image(image_path)

def main():
    # Argument parser to handle multiple image paths
    parser = argparse.ArgumentParser(description="Update timezone info for images based on GPS EXIF data.")
    parser.add_argument('image_paths', nargs='+', help='Paths to images (use wildcard for multiple files)')
    
    args = parser.parse_args()
    
    # Expand wildcard arguments (e.g., ./imagefolder/*)
    image_files = []
    for path in args.image_paths:
        image_files.extend(glob.glob(path))
    
    # Remove directories from the list (only process files)
    image_files = [f for f in image_files if os.path.isfile(f)]
    
    # Process the images
    update_images_timezone(image_files)

if __name__ == "__main__":
    main()