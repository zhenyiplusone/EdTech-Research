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
drop REGION
unab tilt: r_* m_* s_* w_* h_*
reshape wide `tilt', i(CAMPUS DNAME CNAME YEAR) j(GRADE) string
merge m:1 CAMPUS using Directory.dta
keep if _merge == 3
drop _merge

save texas_cleaned_2, replace