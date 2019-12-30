# NGSIM US-101 Dataset Smoothing

### Description

*NGSIM US-101 Dataset Smothing* provides a less-noisy and smoothed version of the well known trajectory NGSIM US-101 dataset using **[Savitzky-Golay Filter](https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.savgol_filter.html)**. The Smoothing is done as a two step process which is composed of first, smothing the X and Y values, then recomputing velocities and acceleration with respect to the smoothed X, Y values.

### Table of Content

1. [About The NGSIM US-101 Dataset]()
2. [Smoothing approach]()
3. [How to use]() 


### About The NGSIM US-101 Dataset
The NGSIM US 101 datatset has been the ultimate open source dataset for trajectory prediction for researchers since its release in 2005. Many Researchers including [1-3] have pointed out the presence of noise in the dataset, mainly due to the fact that it has been automatically extracted from video recordings of 8 cameras mounted over buildings overlooking the Hollywood Freeway, in Los Angeles, CA, also known as southbound US 101. The software used for the extraction of the NGSIM US-101 dataset is called, In addition, the NGSIM documentation explicitly says: 

> <span style="color:red"> no accuracy assessment has been performed for the data set
> 
> <span style="color:red">[We do] not make any claims regarding data completeness. There
may be gaps in the data provided </span>

Some useful links for more details on the NGSIM dataset 
* [Website]() the official dataset webpage
* [Fact sheet]() a fact sheet about the dataset
* [NGSIM project webpage]()



### Smoothing approach:
1.	Smooth positions, then differentiate velocities and acceleration
2.	Differentiate velocities and accelerations, then smooth all three variables
3.	Smooth positions, differentiate velocities, smooth velocities, differentiate acceleration, smooth acceleration


### References
[1] Montanino, Marcello, and Vincenzo Punzo. "*Making NGSIM data usable for studies on traffic flow theory: Multistep method for vehicle trajectory reconstruction.*" Transportation Research Record 2390.1 (2013): 99-111.

[2] Thiemann, Christian, Martin Treiber, and Arne Kesting. "*Estimating acceleration and lane-changing dynamics from next generation simulation trajectory data.*" Transportation Research Record 2088.1 (2008): 90-101.

[3] Altché, Florent, and Arnaud de La Fortelle. "An LSTM network for highway trajectory prediction." 2017 IEEE 20th International Conference on Intelligent Transportation Systems (ITSC). IEEE, 2017.
