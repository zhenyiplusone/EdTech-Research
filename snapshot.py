'''
# Race
DPETBLAP	
DPETHISP	
DPETWHIP	
DPETINDP	
DPETASIP	
DPETPCIP	
DPETTWOP

# Econ disadvan (free lunch)
DPETECOP


# Student to teacher ratio

DPSTKIDR

# Averge staff experience

DPSTEXPA
'''

import pandas as pd
import numpy as np

def combine_and_clean():
	combined_snapshot = pd.DataFrame(columns = ['YEAR', 'DISTRICT', 'DistrictPBlack', 
		'DistrictPHispanic', 'DistrictPWhite', 'DistrictPIndian', 'DistrictPAsian', 'DistrictPPacific',
		'DistrictPTwo', 'DistrictPFreeReduced', 'DistrictStuTeachRatio', 'DistrictAverageStaffExp'])
	for year in range(12, 20):
		ss = pd.read_excel(f'District Snapshots\DistrictProfile{year}.xls')
		ss = ss[['DISTRICT', 'DPETBLAP', 'DPETHISP', 'DPETWHIP', 'DPETINDP', 'DPETASIP', 'DPETPCIP', 
		'DPETTWOP', 'DPETECOP', 'DPSTKIDR', 'DPSTEXPA']]
		ss['YEAR'] = 2000 + year
		ss = ss.rename(columns={"DPETBLAP": "DistrictPBlack", 
			"DPETHISP": "DistrictPHispanic",
			"DPETWHIP": "DistrictPWhite",
			"DPETINDP": "DistrictPIndian",
			"DPETASIP": "DistrictPAsian",
			"DPETPCIP": "DistrictPPacific",
			"DPETTWOP": "DistrictPTwo",
			"DPETECOP": "DistrictPFreeReduced",
			"DPSTKIDR": "DistrictStuTeachRatio",
			"DPSTEXPA": "DistrictAverageStaffExp"})
		combined_snapshot = combined_snapshot.append(ss, ignore_index=True)
	combined_snapshot['DistrictStuTeachRatio'] = pd.to_numeric(combined_snapshot['DistrictStuTeachRatio'], downcast='float', errors='coerce')
	combined_snapshot['DistrictAverageStaffExp'] = pd.to_numeric(combined_snapshot['DistrictAverageStaffExp'], downcast='float', errors='coerce')
	combined_snapshot.loc[combined_snapshot['DistrictStuTeachRatio'] < 0, ['DistrictStuTeachRatio']]=np.nan

	combined_snapshot.to_excel("District Snapshots\Combined District Profile.xls",index=False)

combine_and_clean()

