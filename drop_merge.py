import pandas as pd 

Texas_DB = pd.read_stata('texas_cleaned_4.dta')
print(Texas_DB.shape)
Texas_DB.drop(Texas_DB[Texas_DB["_districtmerge"] == "merged (3)"].index, inplace = True)
print(Texas_DB.shape)
#Texas_DB.to_stata('texas_cleaned_4.dta', write_index = False) 