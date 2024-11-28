'''
File: ./README.md
'''
This python package could refine Period-Luminosity relation of variable stars for given  Cepheid dataset. Dataset must be stored in './data/input/' directory where './' is folder of 'README.md'. 

My dataset contains 95 Galactic Cepheids:

	Metadata		Column	Reference
1) INDEX 			  1	
2) Color excess, E(B-V) 	  1 	Fernie 1995
3) distance modulus, mu 	  1	Gaia 2023, IRSB 2011
4) Period of Cepheid, log P	  1	
5) Photometry	BVIJHK		  6	Jesper 2011

In the analysis, color excess will be converted in extinction using Table 4 of Fouque (2007) which fundametally derived from extinction law (Cardelli, 1989) and R(V) = 3.23 (Sandage 2004). Also, reddening free magnitudes are calculated using Wesenhiet function (Madore, 1982) which fudamentally derived from reddening ratio, R. 
-- Read the extinction law and reddening ratio formulation in './lvtlaw/utils.py'.

Initially, raw PL and PW relation is derived using linear regression module, then their residues are correlated and reddening correction estimated by adjusting distance modulus error. basic idea is, in the absence of distance error, residual slope approaches to infinity (parallel to y-axis), in the absence of reddening error, the slope approaches to 1. 

Adjusting raw luminosity by estimated distance-reddening error pair for each Cepheid, the calibrated PL relation is determined. 
