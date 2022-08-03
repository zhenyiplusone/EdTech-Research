import pandas as pd

df = pd.read_stata('texas_cleaned_4_with_snapshot.dta')

max_vars = ['m_all_d03', 'r_all_d04', 's_all_d05', 'm_all_d06', 'm_all_d07', 'r_all_d08']
diff_vars = {'m_all_d03': ['r_all_d03'], 
	'r_all_d04': ['m_all_rs04', 'w_all_rs04'], 
	's_all_d05': ['r_all_rs05','m_all_rs05'], 
	'm_all_d06': ['r_all_rs06'], 
	'm_all_d07': ['r_all_rs07', 'w_all_rs07'], 
	'r_all_d08': ['m_all_rs08', 's_all_rs08','h_all_rs08']
}

for max_var in max_vars:
	df_max_more_equal_5 = df[df[max_var] > 4]
	for diff_var in diff_vars[max_var]:
		df_diff_more_equal_5 = df[df[diff_var] > 4]
		diff = df_max_more_equal_5.shape[0] - df_diff_more_equal_5.shape[0]
		print(f'The different btwn {max_var} and {diff_var} is {diff}')