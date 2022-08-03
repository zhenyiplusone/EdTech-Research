use texas_cleaned_4_with_snapshot.dta, clear
gen logDisDisbursement = ln(1+DisTotalAuthorizedDisbursement)
egen CAMPUSID = group(CAMPUS)
sort CAMPUSID YEAR
quietly by CAMPUSID YEAR: gen dup = cond(_N==1,0,_n)
drop if dup>1
drop dup
xtset CAMPUSID YEAR

local staarTestAverages r_all_rs03 m_all_rs03 r_all_rs04 m_all_rs04 w_all_rs04 r_all_rs05 m_all_rs05 s_all_rs05 r_all_rs06 m_all_rs06 r_all_rs07 m_all_rs07 w_all_rs07 r_all_rs08 m_all_rs08 s_all_rs08 h_all_rs08

local staarTestNDocs r_all_do~n03 m_all_do~n03 r_all_do~n04 m_all_do~n04 w_all_do~n04 r_all_do~n05 m_all_do~n05 s_all_do~n05 r_all_do~n06 m_all_do~n06 r_all_do~n07 m_all_do~n07 w_all_do~n07 r_all_do~n08 m_all_do~n08 s_all_do~n08 h_all_do~n08

local n_tests : word count `staarTestAverages'

*for loop basically goes through each grade and each subject to generate an excel output
forvalues i = 1/`n_tests' {
	* gets the current test score average in the for loop
	local currAvg `:word `i' of `staarTestAverages''
	* gets the current number of current tests submitted in the for loop
	local currDocs `:word `i' of `staarTestNDocs'' 
	
	local indpVar logDisDisbursement `currDocs' DistrictPBlack DistrictPHispanic DistrictPWhite DistrictPIndian DistrictPAsian DistrictPPacific DistrictPTwo 	DistrictPFreeReduced DistrictStuTeachRatio DistrictAverageStaffExp UnemploymentRate MedianHouseholdIncome Population WifiConnectionPer1000

	xtreg `currAvg' `indpVar', fe
	outreg2 using Table3/`currAvg'.xls, excel replace sideway
}
