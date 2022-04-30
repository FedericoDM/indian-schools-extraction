# Objeto - Extractor de Info de Tanzania

import re
import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


class TanzaniaScrapper:
    def __init__(self, base_url, year, headers):
        self.base_url = base_url
        self.year = year
        self.headers = headers

    def create_session(self):
        """
        Create Session with base_url
        """
        with requests.Session() as session:
            session.get(self.base_url, self.headers)

        return self.session

    def get_regions_dict(self):
        """
        Get the regions dictionary from the base url

        Parameters
        ----------
        base_url : str
        """

        # Connect to the base url
        r = requests.get(self.base_url, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")

        # Parse html and get regions
        a_objects = soup.find_all("a")
        unwanted_chars = ["\r", "\n"]
        regions_dict = {}

        for a_object in a_objects:
            href = a_object["href"]
            region_name = a_object.text

            # Remove unwanted characters
            for unwanted_char in unwanted_chars:
                region_name = region_name.replace(unwanted_char, "")

            region_url = self.base_url.replace("psle.htm", href)
            regions_dict[region_name] = region_url

        return self.regions_dict
