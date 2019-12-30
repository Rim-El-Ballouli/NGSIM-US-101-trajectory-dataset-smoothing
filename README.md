# NGSIM US-101 Dataset Smoothing

### Description

*NGSIM US-101 Dataset Smothing* provides a less-noisy and smoothed version of the well known trajectory NGSIM US-101 dataset using **[Savitzky-Golay Filter](https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.savgol_filter.html)**. The Smoothing is done as a two step process which is composed of first, smothing the X and Y values, then recomputing velocities and acceleration with respect to the smoothed X, Y values.

### Table of Content

1. [The NGSIM US-101 Dataset]()
2. [Smoothing approach]()
3. [How to use]() 


### The NGSIM US-101 Dataset
The NGSIM US 101 datatset has been the ultimate open source dataset for trajectory prediction for researchers since its release in 2005. Many Researchers including [1-3] have pointed out the presence of noise in the dataset, mainly due to the fact that it has been automatically extracted from video recordings of 8 cameras mounted over buildings overlooking the Hollywood Freeway, in Los Angeles, CA, also known as southbound US 101. The software used for the extraction of the NGSIM US-101 dataset is called NG-VIDEO software. In addition, the NGSIM documentation explicitly says: 

> no accuracy assessment has been performed for the data set
> 
> [We do] not make any claims regarding data completeness. There
>may be gaps in the data provided

We found that when plotting acceleration against time, for some vehicles, there is a hard acceleration and deceleration in few seconds, which is unrealistic. Also we found that 8.99% of the dataset has an unrealistic acceeration above 3 m/s^2.


For more details on the NGSIM dataset, here are Some useful links 
* [Website](https://data.transportation.gov/Automobiles/Next-Generation-Simulation-NGSIM-Vehicle-Trajector/8ect-6jqj) the official dataset webpage
* [Fact sheet](https://www.fhwa.dot.gov/publications/research/operations/07030/index.cfm) about the dataset
* [NGSIM project webpage](https://ops.fhwa.dot.gov/trafficanalysistools/ngsim.htm)


### Smoothing approach:
There are three main approaches that can be used to smooth the dataset, which are:

1.	Smooth all four variables i.e. X, Y, velocities and accelerations
2.	Smooth X, and Y, then differentiate velocities and acceleration
3.	Smooth X and Y, then differentiate velocities, smooth velocities, differentiate acceleration, and finally smooth acceleration

We rely on the second approach and we use the [Savitzky-Golay filter](https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.savgol_filter.html) implemented in the python scipy.signal library

### Requirments
	
conda environment
3.6 pythong

how to use 

### References
[1] Montanino, Marcello, and Vincenzo Punzo. "*Making NGSIM data usable for studies on traffic flow theory: Multistep method for vehicle trajectory reconstruction.*" Transportation Research Record 2390.1 (2013): 99-111.

[2] Thiemann, Christian, Martin Treiber, and Arne Kesting. "*Estimating acceleration and lane-changing dynamics from next generation simulation trajectory data.*" Transportation Research Record 2088.1 (2008): 90-101.

[3] Altché, Florent, and Arnaud de La Fortelle. "An LSTM network for highway trajectory prediction." 2017 IEEE 20th International Conference on Intelligent Transportation Systems (ITSC). IEEE, 2017.
