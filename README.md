# vSWIM<sup>beta</sup> - A Virtual Solar Wind Monitor for Mars 

### IMPORTANT: This repository is currently in beta and has been released for the peer review process (as of February 1, 2024). 

This repository contains predictions of the solar wind upstream of Mars from late 2014 onwards as calculated from [MAVEN](https://mars.nasa.gov/maven/) spacecraft data and a machine learning model.  

### Contents

1. **Low Resolution Data:** Hourly cadence solar wind predictions at [INSERT]. Use this if you need an [OMNI-like](https://omniweb.gsfc.nasa.gov/form/dx1.html) product at Mars.
2. **Code:** Source code needed to generate predictions at [INSERT]. Use this if you need sub hour predictions of the solar wind at Mars.
3. **Usage Guidelines:** A short user guide for vSWIM. Read this if you need to use either 1 or 2.

### User Guide

[1. Model Description](#model)
   
[2. Assessment](#assessment)

[3. Suggested Use Cases](#usecases)

[4. Limitations](#limits)
 
 <!-- headings -->
 <a id="model"></a>
 ### 1. Model Description

   <details>
   <summary>Overview:</summary>
   
   This model uses solar wind data measured from the MAVEN spacecraft since late 2014 and Gaussian process regression to generate continuous predictions (mean, $\mu$ and standard deviation, $\sigma$) of mulitple features of the solar wind including: 
   
   - IMF: $B_{x}$, $B_{y}$, $B_{z}$, and $|B|$ in [nT]
   - Velocity: $V_{x}$, $V_{y}$, $V_{z}$, and $|V|$ in [km/s]
   - Temperature: $T_{p}$ in [eV]
   - Pressure: $n_{p}$ in [per cc]
   
   All vector quanties are measured in Mars Solar Orbital (MSO) coordinates. </details>
   
   <details>
   <summary>Data sources:</summary>
   
   The original data used in for this process is from a combined SWIA and MAG (MAVEN instruments) data source, see [Halekas+2017](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016JA023167), [Halekas+2015](https://link.springer.com/article/10.1007/s11214-013-0029-z), [Connerney+2015](https://link.springer.com/article/10.1007/s11214-015-0169-4) and [online](https://homepage.physics.uiowa.edu/~jhalekas/drivers.html) for original data.</details>
   
   <details>
   <summary>Implementation</summary>

   We treat each feature seperately and discretize the entire dataset into subsets of 1,000 points before running a Gaussian process regression in [GPFlow](https://gpflow.github.io/GPflow/2.9.0/index.html). 
   
   y (solar wind feature) outputs are normalized to their mean and standard deviation of the subset, x (time) is normalized between 0 and 100. We use a zero mean function and a [RationalQuadratic] covariance fucntion (https://gpflow.github.io/GPflow/develop/api/gpflow/kernels/index.html) kernel with: l initialized to 0.1 of the non zero gaps betwen the dataset and ranging from the minimum to the median of the non zero gaps, and the variance intitially set to 3. A fuller discussion of implementation Gaussian processes can be found within [Azari et al., 2024](PENDING).</details>
   
   <details>
   <summary>Example Algorithm</summary>
   
   - Split MAVEN dataset into 1000 datapoint subsets
   - For each subset
        - For each feature in the dataset $y_{i}$) where i ranges from {0, ..., 9}, corresponding to each unique solar wind feature
           - Normalize inputs
           - Initialize kernel hyperparameters
           - Run Gaussian process regression
           - Return predictions and unnormalize</details>

 
  <a id="asssessment"></a>
 ### 2. Assessment 
 
  <a id="usecases"></a>
 ### 3. Suggested Use Cases
 
  <a id="limits"></a>
 ### 4. Limitations

 WILL PREDICT THE MEAN
 
The following describes the suggested uses and limitations of the vSWIM model. It follows a rough standard AI model reporting in model card format (see [Mitchell et al., 2015](https://dl.acm.org/doi/10.1145/3287560.3287596)). A more extensive overview can be found within [Azari et al., 2024](PENDING).

#### Model Description

Overview: This model is a Gaussian process regression on high-resolution upstream data from MAVEN SWIA and MAG from 2014 up to present.

Original data source: 

Outputs: 

#### Performance

(test set) refer people to paper.  

#### Suggested Usage

#### Limtations

### Citing vSWIM

If you use this product please reference the submitted [JGR Machine Learning paper](PENDING). Sample Bibtex is given below:

```
@article{Azari2024,
author = {Azari A. R. and Abrahams, E. and Sapienza, and F. and Halekas, J. and Biersteker, J. and 
Mitchell, D. L. and P ́erez, F. and Marquette, M. and Rutala, M. J. and Bowers, C. F. and 
Jackman, C. M. and Curry, S. M.},
doi = {TBD},
journal = {Journal of Geophysical Research: Machine Learning and Computation},
title = {A Virtual Solar Wind Monitor for {M}ars with Uncertainty Quantification using {G}aussian Processes},
year = {2024, submitted}
}
```
