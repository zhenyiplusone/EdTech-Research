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
/*merge m:m SCHOOLADDRESSIDENTIFIER YEAR using SchoolDetailedReport.dta
rename CommittedAmount SchCommittedAmount
rename CmtdTotalCost SchCmtdTotalCost
rename TotalAuthorizedDisbursement SchTotalAuthorizedDisbursement
rename _merge _schoolmerge*/

merge m:m DISTRICTADDRESSIDENTIFIER YEAR using DistrictDetailedReport.dta
rename CommittedAmount DisCommittedAmount
rename CmtdTotalCost DisCmtdTotalCost
rename TotalAuthorizedDisbursement DisTotalAuthorizedDisbursement
rename _merge _districtmerge
save texas_cleaned_3_with_funding, replace