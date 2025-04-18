# File: ./README.md

# Purpose
This python package can refine Period-Luminosity relation of Cepheid variable stars.

# Execution
Clone the repo and simply run the main.py file. 

	python3 main.py

# Background
This linear correlation between period and luminiosity was discovered by Mrs. Henry Leavitt in 1908, that's why it is also called as Leavitt Law. In astronomy, this relation is very important as it serves as a tool for measuring distances to distant galaxies. The realization of Milky Way as an isolated galaxy (1918), the expansion of the Universe (1924), rotation of Milky Way (1934), estimation of age of universe (1958), standardization of cosmic distance ladder (1995), and so on are derived results from the Leavitt Law.   

# Motivation
Scatter in linear period-luminosity relation limits the accuracy of this method upto few MPc (mega parsec - unit of length). This python package reduce the scatter by determining the systemtic error in the raw dataset, extending the outreach of the PL relations by constraining the zero-point offset of the linear relation. 

# Data
For calibration, multiband photometry data (here BVIJHK bands) of each Cepheid star, impact of interstellar dust on the intensity of incoming light (interstellar reddening) and distances to each star would be required.

Dataset must be stored in .csv file in './data/input/' directory where './' is folder of 'README.md' file (this file). 

Current sampled dataset contains 95 Galactic Cepheids:

	Metadata		Column	Reference
1) INDEX 			  1	
2) Period of Cepheid, log P	  1	
3) Color excess, E(B-V) 	  1 	Fernie 1995
4) distance modulus, mu 	  1	Gaia 2023, IRSB 2011
5) Photometry	BVIJHK		  6	Jesper 2011

# Method
Intially, color excess (interstellar reddening) will be converted to extinction in each band using Table 4 of Fouque (2007) which fundametally derived from extinction law (Cardelli, 1989) and R(V) = 3.23 (Sandage 2004). Also, reddening free magnitudes are calculated using Wesenhiet function (Madore, 1982) which fudamentally derived from reddening ratio, R. 
-- Read the extinction law and reddening ratio formulation in './lvtlaw/utils.py'.

From the raw data, absolute magnitude, 'true' absolute magnitude and wesenheit magnitude will be derived. See the file './lvtlaw/data_transform.py'. 

The raw PL and PW relation is derived using linear regression module ('./lvtlaw/pl_pw.py'), then their residues are correlated ('./lvtlaw/residue.py') to decouple the source of systematic error in distance and extinction. By adjusting the distance, variation in extinction over wavelength is traced. Distance error yielding the same reddening correction for all band will be considered the ideal correction pair for distace and reddening error ('./lvtlaw/error_estimate.py'). 

Fundamental idea is, in the absence of distance error, residual slope approaches to infinity (parallel to y-axis), in the absence of reddening error, the slope approaches to 1 and in the absence of both error, all the points will clustered around the origin.  

Adjusting raw data with the estimated distance-reddening error pair for each Cepheid, then the calibrated PL relation is determined. 

# Documentation
Read the 'Physics_Modelling_and_Results.pdf' to learn about the physics behind the topic.

# Credits
The Raw Dataset of 150 Cepheid stars is provided by my supervisor: Dr Jesper Storm (AIP Potsdam) 

The calibration method developed by Dr. Barry Madore (https://iopscience.iop.org/article/10.3847/1538-4357/aa6e4d/pdf). 

Mathematical model of the algorithm developed by me. By correlating model with physics, I developed more generalized algorithm which yields better results than the previous method. 

The complete python code is developed by me and can be used by anyone without asking for any permission from me.

