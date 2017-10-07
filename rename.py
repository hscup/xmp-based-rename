import sys
import os
from bisect import bisect
from PIL import Image, ImageFilter

import logging
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S:', filename='log.txt', level=logging.ERROR)

# Track the number of duplicate file name
fname_counts = {}


def get_direction(yawdegree,
                  breakpoints=[-157.5, -112.5, -67.5, -22.5,
                               +22.5, +67.5, +112.5, +157.5],
                  directions=['SOUTHFACING', 'SOUTHWESTFACING', 'WESTFACING',
                              'NORTHWESTFACING', 'NORTHFACING', 'NORTHEASTFACING',
                              'EASTFACING', 'SOUTHEASTFACING', 'SOUTHFACING']):
    i = bisect(breakpoints, yawdegree)
    return directions[i]


def bulk_rename(images_dir):
    images_files = [os.path.join(images_dir, f) for f in os.listdir(
        images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    for image_file in images_files:
        try:
            rename(image_file, images_dir)
        except Exception as ex:
            logging.error(ex)


def rename(image_file, output_dir="."):
    iamge_name, image_extension = os.path.splitext(image_file)
    new_name = None
    with Image.open(image_file, 'r') as im:
        for segment, content in im.applist:
            marker, body = content.split(b'\x00', 1)
            # Check if there image has XMP metadata
            if segment != 'APP1' or marker != b'http://ns.adobe.com/xap/1.0/':
                continue

            # Find the FlightYawDegree field
            start = body.find(b'FlightYawDegree="')
            if start == -1:
                continue
            start += len(b'FlightYawDegree="')
            end = body.find(b'"', start)
            if end <= start:
                continue

            yaw_degree = float(body[start:end])
            direction = get_direction(yaw_degree)
            duplicate_count = get_number_duplicate(
                direction + image_extension.lower())
            
            # If there is existing file with same name then add a number
            if duplicate_count > 1:
                new_name = os.path.join(
                    output_dir, direction + str(duplicate_count) + image_extension)
            else:
                new_name = os.path.join(
                    output_dir, direction + image_extension)

    if new_name:
        os.replace(image_file, new_name)


def get_number_duplicate(filename):
    if filename in fname_counts:
        fname_counts[filename] += 1
    else:
        fname_counts[filename] = 1
    return fname_counts[filename]


def usage():
    print("""
        Usage:
            python rename.py <images_directory>

        Example:
            python rename.py "C:\\Data\\images"
    """)

def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
    # Get image dir from argument
    images_dir = sys.argv[1]
    if not os.path.isdir(images_dir):
        usage()
        sys.exit('Exit: "{}" is not a directory'.format(images_dir))

    bulk_rename(images_dir)

if __name__ == "__main__":
    main()
