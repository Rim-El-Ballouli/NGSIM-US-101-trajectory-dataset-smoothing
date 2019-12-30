# NGSIM US-101 Dataset Smoothing

#### Description

*NGSIM US-101 Dataset Smothing* provides a non-noisy and smoothed version of the well known trajectory NGSIM US-101 dataset using **Savitzky-Golay Filter**. 

#### About The NGSIM US-101 Dataset
The NGSIM datatset has been the ultimate open source dataset for trajectory prediction for researchers since its release in 2005.
Researchers have pointed out presence of noise in the dataset, mainly due to the fact that it has been automatically extracted from 8 camera recordings over the  road.
This project relies on smoothing the 


Some useful links on NGSIM dataset 
* [Website]() the official dataset webpage
* [Fact sheet]() a fact sheet about the dataset
* [NGSIM project webpage]()


#### Smoothing approach:
1.	Smooth positions, then differentiate velocities and acceleration
2.	Differentiate velocities and accelerations, then smooth all three variables
3.	Smooth positions, differentiate velocities, smooth velocities, differentiate acceleration, smooth acceleration


