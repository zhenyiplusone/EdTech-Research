program define clean
	quietly ds, has(varlabel "*Grade Level*" "*Avg Items*")
	local delete r(varlist)

	foreach col in `r(varlist)'{
		drop `col'
	}

	quietly ds, has(varlabel "*Risk*" "*Special*" "*Gifted*" "*LEP*" "*Title*" "*Participant*" "*ESL*" "*Language*" "*Bilingual*" "*Migrant*" "*Econ*" "*Meals*" "*Career*" "*Homeless*")
	local delete r(varlist)

	foreach col in `r(varlist)'{
		drop `col'
	}

end 
import sas using "STAAR/cfy12e3.sas7bdat", clear
clean
save texas.dta, replace
local filenamelist "STAAR/cfy12e4.sas7bdat STAAR/cfy12e5.sas7bdat STAAR/cfy12e6.sas7bdat STAAR/cfy12e7.sas7bdat STAAR/cfy12e8.sas7bdat STAAR/cfy13e3.sas7bdat STAAR/cfy13e4.sas7bdat STAAR/cfy13e5.sas7bdat STAAR/cfy13e6.sas7bdat STAAR/cfy13e7.sas7bdat STAAR/cfy13e8.sas7bdat STAAR/cfy14e3.sas7bdat STAAR/cfy14e4.sas7bdat STAAR/cfy14e5.sas7bdat STAAR/cfy14e6.sas7bdat STAAR/cfy14e7.sas7bdat STAAR/cfy14e8.sas7bdat STAAR/cfy15e3.sas7bdat STAAR/cfy15e4.sas7bdat STAAR/cfy15e5.sas7bdat STAAR/cfy15e6.sas7bdat STAAR/cfy15e7.sas7bdat STAAR/cfy15e8.sas7bdat STAAR/cfy16e3.sas7bdat STAAR/cfy16e4.sas7bdat STAAR/cfy16e5.sas7bdat STAAR/cfy16e6.sas7bdat STAAR/cfy16e7.sas7bdat STAAR/cfy16e8.sas7bdat STAAR/cfy17e3.sas7bdat STAAR/cfy17e4.sas7bdat STAAR/cfy17e5.sas7bdat STAAR/cfy17e6.sas7bdat STAAR/cfy17e7.sas7bdat STAAR/cfy17e8.sas7bdat STAAR/cfy18e3.sas7bdat STAAR/cfy18e4.sas7bdat STAAR/cfy18e5.sas7bdat STAAR/cfy18e6.sas7bdat STAAR/cfy18e7.sas7bdat STAAR/cfy18e8.sas7bdat STAAR/cfy19e3.sas7bdat STAAR/cfy19e4.sas7bdat STAAR/cfy19e5.sas7bdat STAAR/cfy19e6.sas7bdat STAAR/cfy19e7.sas7bdat STAAR/cfy19e8.sas7bdat"
display "`filenamelist'"
foreach filename in `filenamelist'{
	import sas using `filename', clear
	clean
	save "temp.dta", replace
	use texas.dta
	append using temp.dta
	save texas.dta, replace
}
/*  STAAR/cfy12e5.sas7bdat STAAR/cfy12e6.sas7bdat STAAR/cfy12e7.sas7bdat STAAR/cfy12e8.sas7bdat STAAR/cfy13e5.sas7bdat STAAR/cfy13e6.sas7bdat STAAR/cfy13e7.sas7bdat STAAR/cfy13e8.sas7bdat */
use texas.dta
clean
drop REGION 
drop _merge
unab tilt: r_* m_* s_* w_* h_*
reshape wide `tilt', i(CAMPUS DNAME CNAME YEAR) j(GRADE) string
save texas2, replace


import delimited using "Directory.csv", clear
split schoolnumber, parse(') generate(schoolnumbersplit)
rename schoolnumbersplit2 CAMPUS
split schoolzip, parse(-) generate(schoolzipsplit)
split schoolsitestreetaddress
egen SCHOOLADDRESSIDENTIFIER = concat(schoolzipsplit1 schoolsitestreetaddress1), punct("_")
split districtzip, parse(-) generate(districtzipsplit)
split districtsitestreetaddress
egen DISTRICTADDRESSIDENTIFIER = concat(districtzipsplit1 districtsitestreetaddress1), punct("_")
keep CAMPUS SCHOOLADDRESSIDENTIFIER DISTRICTADDRESSIDENTIFIER
save Directory.dta, replace

use texas_cleaned.dta
merge m:1 CAMPUS using Directory.dta
keep if _merge == 3
drop _merge
split DNAME, generate(districtname)
split CNAME, generate(campusname)
egen NEWDISTRICTADDRESSIDENTIFIER = concat(districtname1 DISTRICTADDRESSIDENTIFIER), punct("-")
egen NEWSCHOOLADDRESSIDENTIFIER = concat(campusname1 SCHOOLADDRESSIDENTIFIER), punct("-")
drop DISTRICTADDRESSIDENTIFIER
drop SCHOOLADDRESSIDENTIFIER
rename NEWSCHOOLADDRESSIDENTIFIER SCHOOLADDRESSIDENTIFIER
rename NEWDISTRICTADDRESSIDENTIFIER DISTRICTADDRESSIDENTIFIER

save texas_cleaned_2, replace

import delimited using "SchoolDetailedReport2018.csv", clear
split applicantstreetaddress1
split billedentityname
egen SCHOOLADDRESSIDENTIFIER = concat(billedentityname1 applicantzipcode applicantstreetaddress11), punct("-")
destring cmtdtotalcost cmtdfundingrequest, generate(schooltotalcost schooltotalfunded) ignore("$ ,%")
keep billedentityname schooltotalcost schooltotalfunded SCHOOLADDRESSIDENTIFIER benurbanruralstatus
collapse (sum) schooltotalcost schooltotalfunded, by(billedentityname SCHOOLADDRESSIDENTIFIER benurbanruralstatus)
save SchoolDetailedReport, replace

import delimited using "DistrictDetailedReport2018.csv", clear
split applicantstreetaddress1
split billedentityname
egen DISTRICTADDRESSIDENTIFIER = concat(billedentityname1 applicantzipcode applicantstreetaddress11), punct("-")
destring cmtdtotalcost cmtdfundingrequest, generate(districttotalcost districttotalfunded) ignore("$ ,%")
keep billedentityname districttotalcost districttotalfunded DISTRICTADDRESSIDENTIFIER benurbanruralstatus
collapse (sum) districttotalcost districttotalfunded, by(billedentityname DISTRICTADDRESSIDENTIFIER benurbanruralstatus)
save DistrictDetailedReport, replace

use teched_2019_experimental.dta

import excel School_Mega_Sheet.xlsx, clear
save SchoolDetailedReport, replace
import excel District_Mega_Sheet.xlsx, clear
save DistrictDetailedReport, replace
import excel TXSchoolDistrictEcon.xlsx, clear
save Texas_District_Econ_Info, replace

use texas_cleaned_2.dta, clear
destring DISTRICT, replace
drop _merge
merge m:1 YEAR DISTRICT using Texas_District_Econ_Info.dta
merge m:m SCHOOLADDRESSIDENTIFIER YEAR using SchoolDetailedReport.dta

save 
rename _merge _schoolmerge
merge m:m DISTRICTADDRESSIDENTIFIER using DistrictDetailedReport.dta


sort SCHOOLADDRESSIDENTIFIER
quietly by SCHOOLADDRESSIDENTIFIER:  gen dup = cond(_N==1,0,_n)
sort DISTRICTADDRESSIDENTIFIER
quietly by DISTRICTADDRESSIDENTIFIER:  gen dup = cond(_N==1,0,_n)


import delimited using "StandardReport.csv", clear
rename billedentityname CAMPUS
rename fundyear YEAR 
tostring YEAR, replace
keep totaldisbursementamount CAMPUS YEAR
save tempcsv.dta, replace
use teched.dta
merge 1:1 CAMPUS YEAR using tempcsv.dta
	
