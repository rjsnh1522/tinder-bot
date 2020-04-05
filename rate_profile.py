import os

import requests
import validators
from functions import FileHandling, download_image, delete_all_files
from secrets import URL_NORMAL, API_KEY, MODEL, OUTPUT_FORMAT


class RateProfile:
    def __init__(self):
        self._url = URL_NORMAL
        self._file_path = None
        self._people = list()
        self.file_read_path = os.path.join('temp')
        self._attractiveness = 0

    def __del__(self):
        delete_all_files(self.file_read_path)

    def set_file_path(self, file_path):
        if validators.url(file_path):
            image_path = download_image(file_path)
            self._file_path = f"{self.file_read_path}/{image_path}"
        else:
            self._file_path = file_path

    def set_people(self, people):
        if isinstance(people, list):
            self._people = people

    def get_attractiveness(self):
        return self._attractiveness

    def rate_pic(self, file_path):
        self.set_file_path(file_path)
        params = (
            ('output', OUTPUT_FORMAT),
            ('apikey', API_KEY),
            ('model', MODEL),
        )
        with FileHandling(self._file_path, 'rb') as file:
            files = file.read()
            response = requests.post(self._url, params=params, data=files)
            json_output = response.json()
            people = json_output['people']
            self.set_people(people)
        self.set_average_attractiveness()

    def set_average_attractiveness(self):
        all_people = len(self._people)
        total_attractiveness = 0
        if all_people > 0:
            for person in self._people:
                total_attractiveness += person['attractiveness']
            average = total_attractiveness/all_people
            self._attractiveness = average


att = RateProfile()
att.rate_pic('')
del att
