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