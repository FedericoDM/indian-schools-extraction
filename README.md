# Indian Schools - Webscraping

The following code provides a _rough_ approach to obtain data from the schools displayed in the following (site)[https://schoolgis.nic.in/],


The folder named **format_data** contains a notebook which concats all the extracted data and formats it as desired.

The folder named **extraction** contains several notebooks used to webscrap the page by using its API. The approach is pretty rough because we iterate the schoolID parameter from 1 to 1,495,000. For that reason, 8 copies of the code were created to extract the data as fast as possible. The bulk_webscraping notebook shows another possible approach that was not fully pursued.
