import requests
import json
import pandas as pd
import numpy as np
import urllib

def download_data():
	for year in range(2015, 2020):
		for grade in range (3,9):
			dls = f"https://tea.texas.gov/sites/default/files/cfy{str(year)[2:]}e{grade}.zip"
			urllib.request.urlretrieve(dls, f"cfy{str(year)[2:]}e{grade}.zip")

download_data()