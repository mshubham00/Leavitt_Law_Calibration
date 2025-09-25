# Leavitt Law Calibration Toolkit
This python package calibrates Period-Luminosity relation of Cepheid variable for incorrect interstellar reddening and distances modulus.

# Execution
1. Clone the repository

	git clone <repo_link>

2. install the require packages from requirements.txt

	pip install -r requirements.txt

3. Add your dataset in ./data/input/<file_name.csv>
4. Map your dataset columns in ./data/datamapping.py
5. Adjust other parameters too in datamapping file: dataset selection (k), save output (s=1), generate plots (p=1)
6. Run the main.py file. 

	python3 main.py

7. To pull updated repo
    
	git pull origin main

# Background of Leavitt Law
A linear correlation between period and luminiosity was discovered by Mrs. Henry Leavitt in 1908. This relation is very important in astronomy as it serves as a tool for measuring distances to distant galaxies. The realization of Milky Way as an isolated galaxy (1918), the expansion of the Universe (1924), rotation of Milky Way (1934), estimation of age of universe (1958), standardization of cosmic distance ladder (1995), and so on are derived results from the Leavitt Law.   
# Motivation
Large scatter in period-luminosity relation limits the accuracy of this method upto few MPc (mega parsec - unit of length). This python package reduce the scatter by determining the systemtic error in the raw measurements, extending the outreach of the PL relations by constraining the zero-point offset. 

# Data
For calibration, multiband photometry data (here BVIJHK bands), interstellar reddening and distances modulus of each Cepheid would be required.

Current sampled dataset contains 95 Galactic Cepheids:

	Metadata		      Column	Reference
1) INDEX 			          1	
2) Period of Cepheid, log P	  1	
3) Color excess, E(B-V) 	  1 	Fernie 1995
4) distance modulus, mu 	  1	    Gaia 2023, IRSB 2011
5) Photometry	BVIJHK		  6	    Jesper 2011


# Data Pipeline
The calibration algorithm is divided into 6 steps. Each written as python modules and stored in ./lvtlaw/<module.py> The first and last two modules are not part of the algorithm.

## ./main.py
main.py sequencely calls functions from lvtlaw.main_modules, which generates stepwise output and saves it as ./data/<file_name>/<step>/<data>.csv

### ./lvtlaw/main_modules.py
This file combines all the components of the algorithm from different modules as functions which called by main.py 

### ./lvtlaw/a_utils.py
It contains supportive functions for algorithm like create directories, linear regression, etc. 
 
### ./lvtlaw/b_data_transform.py
From the raw data, absolute magnitude, 'true' absolute magnitude and wesenheit magnitude will be derived. 

Initially, Color excess (interstellar reddening) will be converted to extinction for each band using Table 4 of Fouque (2007) which fundametally derived from extinction law (Cardelli, 1989) with R(V) = 3.23 (Sandage 2004). 

Reddening free magnitudes are calculated using Wesenhiet function (Madore, 1982) which fudamentally derived from reddening ratio, R. 

### ./lvtlaw/c_pl_pw.py
This derives PL and PW relations, saves the slope, intercept, residues, prediction and generates the plots.

### ./lvtlaw/d_del_del.py
Correlates PL and PW residuals. generate plots and save data. Fundamental idea is, in the absence of distance error, residual slope approaches to infinity (parallel to y-axis), in the absence of reddening error, the slope approaches to 1 and in the absence of both error, all the points will clustered around the origin. 

### ./lvtlaw/e_error_estimation.py
Decouples the source of systematic error in distance and extinction by adjusting the distance. Variation in extinction over wavelength for adjusted distance is traced. Distance error which yields the same reddening correction for all bands is considered as the ideal correction pair for distace and reddening error. 

### ./lvtlaw/f_star_wise.py
For each Cepheid, error pair of reddening and distance estimated by estimating the dispersion in reddening as distance changes.

### ./lvtlaw/g_result.py
Adjusting raw data with the estimated distance-reddening error pair for each Cepheid, then the calibrated PL relation is determined. 

### ./lvtlaw/h_loadoutput.py
Load the processed data for given step.

# Documentation
Read the './docs/Physics_Modelling_and_Results.pdf' to learn about the physics behind the topic.

# Credits
The Raw Dataset of 150 Cepheid stars is provided by my supervisor: Dr Jesper Storm (AIP Potsdam) 

The calibration method developed by Dr. Barry Madore (https://iopscience.iop.org/article/10.3847/1538-4357/aa6e4d/pdf). 

Mathematical model of the algorithm developed by me. By correlating model with physics, I developed more generalized algorithm which yields better results than the previous method. 

The complete python code is developed by me and can be used by anyone without asking for any permission from me.

