# Leavitt Law Calibration Toolkit
This python package calibrates multiband Period-Luminosity relations of Cepheid variable stars available with incorrect interstellar reddening and distances modulus.

# Code Execution
1. Clone the repository

		git clone https://github.com/mshubham00/Leavitt_Law_Calibration.git

2. To pull updated repo
    
		git pull origin main

3. install the require packages from requirements.txt

		pip install -r requirements.txt

4. Add your dataset in ./data/input/<file_name.csv>. Default dataset : 59_madore.csv
5. Map your dataset columns in ./data/datamapping.py. Default : k=0
6. Adjust parameters in datamapping file: extinction_law, reddening_ratio, etc.
7. Run the main.py file. 

		python3 main.py

8. Result in ./data/processed/<file_name.csv>

# Background of Leavitt Law
In 1908, Mrs. Henry Leavitt discovered the linear correlation between pulsation period and luminiosity of nearly-distant Cepheids hosted in SMC galaxy. In astronomy, Leavitt Law serves as a primary standard tool for measuring distances to distant galaxies. The spiral structure of Milky Way (1918), realization of the Milky Way as an isolated galaxy (1924), the expansion of the Universe (1929), rotation of Milky Way (1934), estimation of age of the universe (1958), accelerated expansion of the Universe (1995), Calibration of SNIa based Cosmic Distance Ladder (1998) etc. are a few important results derived from the Leavitt Law. A large scatter in the period-luminosity relation limits the accuracy of distance measurements upto few MPc (mega parsec - unit of length) deep in the observable Universe. This python package reduce the scatter of Leavitt Laws by determining the systemtic error in the reddening and distance measurements of individual Cepheids, ultimately extending the outreach of the Cosmic Distance Ladder. 

# Input Dataset
Pulsation period, multiband photometry data (here BVIJHK bands), approximated interstellar reddening measurement E(B-V) and distances modulus μ of individual Cepheid is required.

Default sampled dataset contains 59 Galactic Cepheids:

	Metadata		      			Column			Reference
	1) INDEX 			          	1	
	2) Period of Cepheid, log P	  	1				Empirically
	3) Color excess, E(B-V) 	  	1 				Fernie 1995
	4) distance modulus, mu 	  	1	    		IRSB 2011
	5) Photometry	BVIJHK		  	6	    		Jesper 2011

# Required Physical measurement
1) Total to selective reddening ratio (Sandage 2004) to convert color excess into bandwise interstellar extinction.
2) Galactic Extinction Law (Fouque 2007) to transform interstellar extinction of V bands into other bands.


# Pipeline Modules
The calibration algorithm is divided into 6 steps. Each written as independent python module stored in ./lvtlaw/<module.py> The first (a_utils.py) and the last two modules (h_loadoutput.py, main_modules.py) do not cover analytical part of the calibration algorithm. 

## ./main.py
main.py sequencely calls functions from lvtlaw.main_modules, which generates stepwise output and saves it as ./data/<file_name>/<step>/<data>.csv

### ./lvtlaw/main_modules.py
This file combines all the components of the algorithm from different modules as functions which called by main.py 

### a: ./lvtlaw/a_utils.py
It contains supportive functions for algorithm like create directories, linear regression, etc. 
 
### b: ./lvtlaw/b_data_transform.py
From the raw data, absolute magnitude, 'true' absolute magnitude and wesenheit magnitude will be derived. 

Initially, Color excess (interstellar reddening) will be converted to extinction for each band using Table 4 of Fouque (2007) which fundametally derived from extinction law (Cardelli, 1989) with R(V) = 3.23 (Sandage 2004). 

Reddening free magnitudes are calculated using Wesenhiet function (Madore, 1982) which fudamentally derived from reddening ratio, R. 

### c: ./lvtlaw/c_pl_pw.py
This derives PL and PW relations, saves the slope, intercept, residues, prediction and generates the plots.

### d: ./lvtlaw/d_del_del.py
Correlates PL and PW residuals. generate plots and save data. Fundamental idea is, in the absence of distance error, residual slope approaches to infinity (parallel to y-axis), in the absence of reddening error, the slope approaches to 1 and in the absence of both error, all the points will clustered around the origin. 

### e: ./lvtlaw/e_error_estimation.py
Decouples the source of systematic error in distance and extinction by adjusting the distance. Variation in extinction over wavelength for adjusted distance is traced. Distance error which yields the same reddening correction for all bands is considered as the ideal correction pair for distace and reddening error. 

### f: ./lvtlaw/f_star_wise.py
For each Cepheid, error pair of reddening and distance estimated by estimating the dispersion in reddening as distance changes.

### g: ./lvtlaw/g_result.py
Adjusting raw data with the estimated distance-reddening error pair for each Cepheid, then the calibrated PL relation is determined. 

### h: ./lvtlaw/h_loadoutput.py
Load the processed data for given step.

# Documentation
Read the './docs/Physics_Modelling_and_Results.pdf' to learn about the physics and mathematical modelling of the calibration algorithm.

# Credits
The calibration method developed by Dr. Barry Madore (https://iopscience.iop.org/article/10.3847/1538-4357/aa6e4d/pdf). 

Mathematical model of the revised algorithm and the complete python code is developed by Shubham Mamgain (I) and can be used by anyone without asking for any permission from me.

