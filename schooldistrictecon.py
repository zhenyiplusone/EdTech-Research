'''
Breaks it from county level to the districts, average each district by the counties in it
'''
import pandas as pd 
import numpy as np 

#Rreads the geography data and the current labels for counties
county_econ = pd.read_excel('TXCountyEcon.xlsx')

geo_df = pd.read_csv('label_geography.csv')
geo_df = geo_df.loc[geo_df["label"].str.contains(", tx", case=False)]
geo_df = geo_df.loc[geo_df["geo_level"]== "C"]
geo_df["label"] = geo_df["label"].apply(lambda x: x.split(", TX")[0])
geo_df["geography"] = geo_df["geography"].apply(lambda x: x[2:]).astype(int)

county_econ['County Name'] = county_econ['CountyID'].apply(lambda x: geo_df.loc[geo_df['geography'] == x]['label'].values[0].title())

# Gets the dataframe of each school district and the counties in it, forming a list
school_dist = pd.read_csv('DistCounty.csv')
school_dist['counties'] = school_dist[['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']].apply(lambda x: x.dropna().tolist(), axis=1)
school_dist = school_dist.drop(['A', 'B', 'C', 'D', 'E', 'F', 'H', 'G', 'I', 'J', 'K'], axis = 1)
print(school_dist)

school_dist_econ = pd.DataFrame(columns = ["District Number", "District Name", "FY", 'Unemployment Rate', 'Median Household Income', 'Population', 'Wifi Connection Per 1000'])

# Averaging the data
for index, district in school_dist.iterrows():
	print(district["District Number"])
	for year in range(2001, 2020):
		df_add = {
		"District Number": district["District Number"],
		"District Name": district["District Name"],
		"FY": year,
		'Unemployment Rate': np.mean([county_econ.loc[(county_econ['FY'] == year) & (county_econ['County Name'] == x.title())].iloc[0]["Unemployment Rate"] for x in district['counties']]),
		'Median Household Income':np.mean([county_econ.loc[(county_econ['FY'] == year) & (county_econ['County Name'] == x.title())].iloc[0]["Median Household Income"] for x in district['counties']]),
		'Population':np.mean([county_econ.loc[(county_econ['FY'] == year) & (county_econ['County Name'] == x.title())].iloc[0]["Population"] for x in district['counties']]),
		'Wifi Connection Per 1000': np.mean([county_econ.loc[(county_econ['FY'] == year) & (county_econ['County Name'] == x.title())].iloc[0]["Wifi Connection Per 1000"] for x in district['counties']])
		}
		school_dist_econ = school_dist_econ.append(df_add, ignore_index = True)


print(school_dist_econ)
print(school_dist_econ.describe())
school_dist_econ.to_excel("TXSchoolDistrictEcon.xlsx",index=False)