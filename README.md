# Webscraping Sideprojects

This repository contains codes for several webscraping one-off projects that I have done. Most of them are in jupyter notebooks because the objective was to extract the data once and then deliver it to the client.

## Indian Schools - BeautifulSoup

The /india folder contains code that provides a _rough_ approach to obtain data from the schools displayed in the following [site](https://schoolgis.nic.in/).

The folder named **format_data** contains a notebook which concats all the extracted data and formats it as desired.

The folder named **extraction** contains several notebooks used to webscrap the page by using its API. The approach is pretty rough because we iterate the schoolID parameter from 1 to 1,495,000. For that reason, 8 copies of the code were created to extract the data as fast as possible. The bulk_webscraping notebook shows another possible approach that was not fully pursued.


## Tanzania Schools - BeautifulSoup


The /tanzania folder contains code that extracts data from the Tanzania schools from this [website](https://onlinesys.necta.go.tz/results/2021/psle/psle.htm).

The notebook contains the  functional code, while the .py contains a class object that was not fully implemented. 

## INE - API Extraction

The /ine folder contains code that was used to extract data from the 2022 mexican presidential poll election. The website is no longer available.

The extract_casillas notebook calls the website's API to extract information per municipality, while the format_data manipulates the resulting dataframes to obtain a cleaner version.


## Colombia - BeautifulSout

Data from all of the schools displayed in the following [page](https://www.redacademica.edu.co/colegios?name=&field_localidad_target_id=All&page=0). The code extracted the characteristics from such schools, and then performed data cleaning to dump the data into a dataframe.

## Colombia Transparency - Selenium Extraction

The /colombia_transparency folder contains a notebook that extracts all of the excel files from the following [page](https://www.chip.gov.co/schip_rt/index.jsf) using Selenium and BeautifulSoup. The code receives the name of a municipality, extracts its historic income data and saves it into a folder.

