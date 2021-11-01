import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
pd.options.mode.chained_assignment = None

Texas_DB = pd.read_stata('texas_cleaned_3_with_funding.dta')

#Need to fix this so it is actually the companies we are missing

Texas_Master_NonMerged_Districts = Texas_DB[Texas_DB["_districtmerge"] == "master only (1)"]
#Texas_Master_NonMerged_Schools = Texas_DB[Texas_DB["_schoolmerge"] == "master only (1)"]

Texas_Using_NonMerged_Districts = Texas_DB[Texas_DB["_districtmerge"] == "using only (2)"]
#Texas_Using_NonMerged_Schools = Texas_DB[Texas_DB["_schoolmerge"] == "using only (2)"]

School_Funding_Data = pd.read_excel('E-Rate_Funding/School_Mega_Sheet_2.xlsx')
District_Funding_Data = pd.read_excel('E-Rate_Funding/District_Mega_Sheet_2.xlsx')

District_Funding_Data = District_Funding_Data[District_Funding_Data['Funding Year'] >= 2012]
School_Funding_Data = School_Funding_Data[School_Funding_Data['Funding Year'] >= 2012]

# Just for testing purposes
#School_Funding_Data = School_Funding_Data.loc[School_Funding_Data['Applicant Name'].shift(1) != School_Funding_Data['Applicant Name']]

def matching(MasterNonMergedDB, UsingNonMergeDB, Funding_DB, NAME, IDEN):
	num = 0
	total = 0
	list_of_apps = []
	print(Funding_DB.columns)
	print(Texas_DB.columns)
	Funding_DB = Funding_DB[(Funding_DB[IDEN].isin(UsingNonMergeDB[IDEN]))]

	#Not finding it cus I matched wronng, forgoot to split into school and district committed funding :D
	for index, row in Funding_DB.iterrows():
		Texas_DB_Right_Year = MasterNonMergedDB[MasterNonMergedDB['YEAR'] == row['Funding Year']]
		Texas_DB_Right_Year[NAME] = Texas_DB_Right_Year[NAME].apply(lambda x: x.replace(" ISD", ""))
		Texas_DB_Right_Year['FuzzyMatch'] = Texas_DB_Right_Year[NAME].apply(lambda x: fuzz.partial_ratio(x, row['Applicant Name']))
		#fuzz.ratio(Texas_DB_Right_Year['CNAME'],row['Applicant Name'])
		highest_val = Texas_DB_Right_Year.loc[Texas_DB_Right_Year['FuzzyMatch'].idxmax()]
		total += 1
		if(highest_val['FuzzyMatch'] > 80 and highest_val[NAME][0] == row['Applicant Name'][0]):
			num+=1
			if f"{row['Applicant Name']} vs {highest_val[NAME]}" not in list_of_apps:
				list_of_apps.append(f"{row['Applicant Name']} vs {highest_val[NAME]} at {highest_val['FuzzyMatch'] }")
				print(f"{row['Applicant Name']} vs {highest_val[NAME]}")
				Texas_DB.loc[(Texas_DB["DNAME"] == f'{highest_val[NAME]} ISD') & (Texas_DB["YEAR"] == row['Funding Year']), 'DisTotalAuthorizedDisbursement'] = row["Total Authorized Disbursement"]
				Texas_DB.loc[(Texas_DB["DNAME"] == f'{highest_val[NAME]} ISD') & (Texas_DB["YEAR"] == row['Funding Year']),"DisCmtdTotalCost"] = row["Cmtd Total Cost"]
				Texas_DB.loc[(Texas_DB["DNAME"] == f'{highest_val[NAME]} ISD') & (Texas_DB["YEAR"] == row['Funding Year']), "DisCommittedAmount"] = row["Committed Amount"]
				Texas_DB.loc[(Texas_DB["DNAME"] == f'{highest_val[NAME]} ISD') & (Texas_DB["YEAR"] == row['Funding Year']), "_districtmerge"] =  "matched (3)"
	print(num/total)
	print(Texas_DB["DisCmtdTotalCost"].count())
	print(Texas_DB.shape)
	Texas_DB.drop(Texas_DB[Texas_DB["_districtmerge"] == "using only (2)"].index, inplace = True)
	print(Texas_DB.shape)
	Texas_DB.to_stata('texas_cleaned_4.dta', write_index = False) 
	#df = pd.DataFrame(list_of_apps)
	#df.to_excel("Matching.xlsx")

#53% of remaining for Districts at 90% threshold
matching(Texas_Master_NonMerged_Districts, Texas_Using_NonMerged_Districts, District_Funding_Data, "DNAME", 'DISTRICTADDRESSIDENTIFIER')

#YIKES 2%
#matching(Texas_Master_NonMerged_Schools, Texas_Using_NonMerged_Schools, School_Funding_Data, "CNAME", 'SCHOOLADDRESSIDENTIFIER')
'''
import excel School_Mega_Sheet.xlsx, firstrow clear 
save SchoolDetailedReport, replace
import excel District_Mega_Sheet.xlsx, firstrow clear
save DistrictDetailedReport, replace

use texas_cleaned_3.dta, clear
destring DISTRICT, replace
merge m:1 YEAR DISTRICT using Texas_District_Econ_Info.dta

drop if _merge != 3
drop _merge
save texas_cleaned_3_with_econ, replace

//Funding.dta?
use texas_cleaned_3_with_econ.dta, clear
merge m:m SCHOOLADDRESSIDENTIFIER YEAR using SchoolDetailedReport.dta

rename _merge _schoolmerge
merge m:m DISTRICTADDRESSIDENTIFIER using DistrictDetailedReport.dta
save texas_cleaned_3_with_funding, replace
'''