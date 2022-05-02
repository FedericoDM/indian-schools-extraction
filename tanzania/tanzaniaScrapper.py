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

    def get_districts_dict(self, region_url):
        """
        Get the districts dictionary from the regions dictionary

        Parameters
        ----------
        regions_dict : dict

        Returns
        -------

        districts_dict : dict
        """
        success = 0
        while success == 0:
            try:
                r = self.session.get(region_url, headers=self.headers, timeout=5)
                success = 1
            except Exception as err:
                time.sleep(1.5)
                print(f"Retrying request: {err}")

        soup = BeautifulSoup(r.content, "html.parser")
        a_objects = soup.find_all("a")

        unwanted_chars = ["\r", "\n"]
        distr_dict = {}

        # Get district dictionary from the region url
        for a_object in a_objects:
            href = a_object["href"]
            distr_name = a_object.text

            for unwanted_char in unwanted_chars:
                distr_name = distr_name.replace(unwanted_char, "")

            # if "results" not in base_url:
            distr_url = self.base_url.replace("psle.htm", f"results/{href}")
            # else:
            # distr_url = base_url.replace("psle.htm", href)

            distr_dict[distr_name] = distr_url

        return self.distr_dict

    def get_schools_dict(self, distr_url):
        """
        Get the schools dictionary from the districts dictionary
        """
        success = 0
        while success == 0:
            try:
                r = self.session.get(distr_url, headers=self.headers, timeout=5)
                success = 1
            except Exception as err:
                time.sleep(1.5)
                print(f"Retrying request: {err}")

        soup = BeautifulSoup(r.content, "html.parser")
        a_objects = soup.find_all("a")

        unwanted_chars = ["\r", "\n"]
        schools_dict = {}

        # Get district dictionary from the region url
        for a_object in a_objects:
            href = a_object["href"]
            school_name = a_object.text

            for unwanted_char in unwanted_chars:
                school_name = school_name.replace(unwanted_char, "")

            school_url = self.base_url.replace("psle.htm", f"results/{href}")

            schools_dict[school_name] = school_url

        return self.schools_dict

    def get_raw_table(self, school_url):

        """
        Gets table with raw data from the school url
        """

        success = 0
        while success == 0:
            try:
                r = self.session.get(school_url, headers=self.headers, timeout=5)
                success = 1
            except Exception as err:
                time.sleep(1.5)
                print(f"Retrying request: {err}")

        soup = BeautifulSoup(r.content, "html.parser")
        raw_tables = soup.find_all("table")

        if len(raw_tables) == 0:
            raw_table = pd.DataFrame([])

        else:
            tables = pd.read_html(r.content)
            raw_table = tables[1]
            raw_table.rename(
                columns={
                    0: "CAND_NO",
                    1: "PREM_NO",
                    2: "SEX",
                    3: "CAND_NAME",
                    4: "SUBJECTS",
                },
                inplace=True,
            )
            raw_table = raw_table.iloc[1:, :]
            raw_table.reset_index(drop=True, inplace=True)

        return self.raw_table

    def get_subjects(self):
        """
        Gets the subjects from the raw table
        """
        unique_subjects = self.raw_table["SUBJECTS"].unique()

        # Asegurarnos de que las materias no sean "*R" o una cosa así
        for unique_subject in unique_subjects:
            if len(unique_subject) > 3:
                str_subjects = unique_subject
                break

        # Caso cuando no hay materias, hardcodearlas
        if (len(unique_subjects) == 1) and ("*" in unique_subjects[0]):
            self.clean_subjects = [
                "Kiswahili",
                "English",
                "Maarifa",
                "Hisabati",
                "Science",
                "Uraia",
                "AverageGrade",
            ]

        else:
            list_subjects = str_subjects.split(",")
            self.clean_subjects = []

            for subject in list_subjects:
                raw_subject = subject.split("-")
                clean_subject = raw_subject[0].replace(" ", "")
                self.clean_subjects.append(clean_subject)

        return self.clean_subjects

    def get_grades(self, num_subjects):
        """
        Gets the grades from the raw table
        """
        str_subjects = self.raw_table["SUBJECTS"]

        # Casos especiales cuando viene una sola letra, poner un vector de NA's
        if (len(str_subjects) <= 3) or ("*" in str_subjects):
            clean_grades = ["NA"] * num_subjects
        else:
            raw_grades = re.findall(r"\s-\s\w+", str_subjects)
            clean_grades = []

            for raw_grade in raw_grades:
                clean_grade = re.findall(r"\w+", raw_grade)
                clean_grade = clean_grade[0]
                clean_grades.append(clean_grade)

        return self.clean_grades
