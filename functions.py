import os
import datetime
import requests
import shutil
from PIL import Image
from six import BytesIO
import re


class FileHandling:
    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.file_name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


def download_image(image_url):
    response = requests.get(image_url, stream=True)
    img = Image.open(BytesIO(response.content))
    file_name = f"{datetime.datetime.now().microsecond}.jpeg"
    img.save(f"temp/{file_name}")
    return file_name


def delete_all_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_url_from_string(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url[0]
