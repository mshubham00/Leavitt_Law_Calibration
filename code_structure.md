main.py calls  
	a_utils	| b_data_transform | f_star_wise | c_pl_pw | d_del_del | e_error_estimation | g_result
Steps:
_________________________________________________________________________________________
a_utils 		output_directories(data_out), load_data(input_data_file) -> df
_________________________________________________________________________________________
b_data_transform  	extinction_law(), transformation(df) - > absolute, extinction, tabsolute, wesenheit
		1_prepared  	_prepared_PLdata.csv
_________________________________________________________________________________________
f_star_wise 		star_frame(prepared_regression_data) -> star_frame_list
_________________________________________________________________________________________
c_pl_pw			pl_reg(prepared_regression_data, s) -> PLW, residue, prediction
				pl_dis(data, dis, bands)
					append_PLW(PLW_struct,i,a,b,c,d,e,f,dis)
		2_PLPW		_residue.csv, _prediction, _regression
_________________________________________________________________________________________
f_star_wise		add_res(star_frame_list, residue) -> star_frame_list
		9_plots	_star.csv	
_________________________________________________________________________________________
d_del_del		residue_analysis(residue, wes_show, flags) -> dres, dpre, dmc
				residue_correlation(residue_file, dis_flag, col, flag)
		3_deldel	del_slope_intercept, del_res, del_pre
_________________________________________________________________________________________
e_error_estimation	reddening_error(wes_show, dis_flag[0], dSM, flags) -> red0_df_list, mu_df_list_dict
				process_reddening(col, dis, slope, intercept, dres, flag, s)
		4_reddening	{len(ext0)}_ext_err0_{col}_{flag}.csv
					error_over_mu(i, col, dis, wm_str, slope, intercept, dres)
						run_mu_for_reddening(ex0, r, slope, intercept)
		5_dispersion	{len(mu_rd_ex_df)}{dis}{wm_str}.csv
_________________________________________________________________________________________
f_star_wise		star_ex_red_mu(n,mu_df_list_dict, df, flags) -> stars_ex_red_mu_list
		6_rms		{n}_{i}stars_ex_red_mu.csv
_________________________________________________________________________________________
g_result		correction_rd_mu(stars_ex_red_mu_list) -> correction_red_mu_stars
				get_error_pair(star, flags, wes_show, del_mu)
		7_errorpair	_error_rms_mu_rd.csv
			correction_apply(tabsolute, correction_red_mu_stars, flags) -> corrected
			corrected_reg(tabsolute, corrected, dis_flag[0], flags, s)
				corrected_PL(tabsolute, corrected, dis, f, s)
					append_PLW(PLW_struct,i,a,b,c,d,e,f,dis)
		8_result	_corrected, i_result_residue, _result_prediction, _result_regression
