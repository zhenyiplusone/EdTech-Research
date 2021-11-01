''' 
Grabs the quarterly labor force data for earned income
'''

import csv
import requests
import json
import pandas as pd

api_key = '799a4f23ccdcbd91cdb606cc2a887c54693c3709'

geo_df = pd.read_csv('label_geography.csv')
geo_df = geo_df.loc[geo_df["label"].str.contains(", tx", case=False)]
geo_df = geo_df.loc[geo_df["geo_level"]== "C"]
geo_df["label"] = geo_df["label"].apply(lambda x: x.split(", TX")[0])
geo_df["geography"] = geo_df["geography"].apply(lambda x: x[2:])

geo_key = dict(zip(geo_df.geography, geo_df.label))
print(geo_key)

final_df = pd.DataFrame()

def grab_quarter_data(quarter, year, data_type, state_num, final_df):
	'''
	Reads it with API
	'''
	url = f'https://api.census.gov/data/timeseries/qwi/sa?get={data_type}&for=county:*&in=state:{state_num}&year={year}&quarter={quarter}&&key={api_key}'
	#x = requests.get(url).json()
	df = pd.read_json(url)
	df = df.rename(columns=df.iloc[0])
	df = df[1:]
	if final_df.empty:
		final_df['county'] = df['county']
	final_df[f'{year}{quarter}'] = df['EarnS'].astype(int)
	return final_df

'''
Goes through all the years for the state of Texas
'''
data_type = "EarnS"
state_num = 48
for year in range(2019,2020):
	for quarter in [3, 4]:
		final_df = grab_quarter_data(quarter, year-1, data_type, state_num, final_df)
	for quarter in [1,2]:
		final_df = grab_quarter_data(quarter, year, data_type, state_num, final_df)
	final_df['total'] = (final_df.iloc[:, 1] + final_df.iloc[:, 2] + final_df.iloc[:, 3] + final_df.iloc[:, 4])*3
	final_df['county_name'] = final_df['county'].apply(lambda x: geo_key[x])
	final_df.to_csv(f'EarnedIncomeTX{year-1-2000}{year-2000}.csv', index=False)

employ_df = pd.read_excel("laucnty19.xlsx")
employ_df = employ_df.rename(columns=employ_df.iloc[1])
employ_df = employ_df[5:]
employ_df = employ_df[employ_df["State"] == "48"]
employ_df = employ_df[["County", "Unemploy-"]]
employ_df['county_name'] = employ_df['County'].apply(lambda x: geo_key[x])
employ_df = pd.merge(final_df, employ_df, on = "county_name")
print(employ_df)
