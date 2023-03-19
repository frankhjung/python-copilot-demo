#!/usr/bin/env python3

"""
Use public API to read daily astronomy picture.

See https://go-apod.herokuapp.com/
"""

import sys

import requests
from PIL import Image


def get_daily_astronomy_image():
    """Read daily astronomy metadata from go-apod.herokuapp.com.

    Returns:
        A dictionary of metadata for the daily astronomy image
    """
    url = "https://go-apod.herokuapp.com/apod"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        print(f"Error: status code {response.status_code}")
        sys.exit(1)
    return response.json()


def show_image(url: str):
    """Read image from url and display to screen.

    Args:
        url: URL of image to be displayed
    """
    # set file name from url
    filename = url.split("/")[-1]
    # stream content from url into a file
    response = requests.get(url, stream=True, timeout=5)
    if response.status_code != 200:
        print(f"Error: status code {response.status_code}")
        sys.exit(1)
    # write stream to file
    with open(filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    # display file to default image viewer
    image = Image.open(filename, mode="r")
    image.show()


def main():
    """Main program. Read daily astronomy image from go-apod.herokuapp.com."""
    data = get_daily_astronomy_image()
    print(data["title"])
    print(data["explanation"])
    show_image(data["url"])


if __name__ == "__main__":
    main()
