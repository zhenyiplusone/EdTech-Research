import pandas as pd 
import numpy as np

def compile():
	df_test = pd.read_stata('texas.dta')

	cols = [c for c in df_test.columns if "_sex" in c or "_all" in c or "_eth" in c]

	df_test = df_test[['CAMPUS','YEAR','REGION','DISTRICT','DNAME','CNAME','GRADE'] + cols]

	cols_drop = [c for c in df_test.columns if c[-3:] =="_rm" or c[-3:] =="_nm"]

	print(df_test)

	df_test.to_stata('texas_cleaned.dta', write_index = False) 

#compile()

def rename_for_match():
	df_test = pd.read_stata('texas_cleaned_2.dta')
	df_test['DISTRICTADDRESSIDENTIFIER'] = df_test["DNAME"].apply(lambda x: x.split(' ')[0]).astype(str) + "_" + df_test["DISTRICTADDRESSIDENTIFIER"]
	df_test['SCHOOLADDRESSIDENTIFIER'] = df_test["CNAME"].apply(lambda x: x.split(' ')[0]).astype(str) + "_" +  df_test["SCHOOLADDRESSIDENTIFIER"]
	df_test['YEAR'] = df_test['YEAR'].apply(int) + 2000
	
	cols_drop = [c for c in df_test.columns if ((c[0] =="w" or c[0] =="s" or c[0] =="h") and  c[-2:] == "03") 
	or ((c[0] =="s" or c[0] =="h") and  c[-2:] == "04")
	or ((c[0] =="w" or c[0] =="h") and  c[-2:] == "05")
	or ((c[0] =="w" or c[0] =="s" or c[0] =="h") and  c[-2:] == "06") 
	or (c[0] =="w" and  c[-2:] == "08")]
	df_test = df_test.drop(cols_drop, axis = 1)
	print(df_test)
	df_test.to_stata('texas_cleaned_3.dta', write_index = False) 
rename_for_match()

#rename for the district committed amount and school committed amount
#Find way for more schools to match