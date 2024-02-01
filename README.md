# vSWIM<sup>*beta*</sup> - A Virtual Solar Wind Monitor for Mars 

### *IMPORTANT: This repository is currently in beta. It has been released for the peer review process.* 

This repository contains predictions of the solar wind upstream of Mars from late 2014 onwards as calculated from [MAVEN](https://mars.nasa.gov/maven/) spacecraft data and the associated predictive model. Largely this model is useful for statistical studies where a continuous estimation with uncertainties is needed at Mars.

## Contents

1. **Low Resolution Data:** Hourly cadence solar wind [predictions](INSERT). Use this if you need an [OMNI-like](https://omniweb.gsfc.nasa.gov/form/dx1.html) product at Mars.
2. **Code:** [Source code](INSERT) needed to generate predictions. Use this if you need sub hour predictions of the solar wind at Mars.
3. **Usage Guidelines:** A short [user guide](#model) for vSWIM. Read this if you need to use the model or the dataset.

<a id="citation"></a>
## Citing vSWIM

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


 <!-- headings -->
 <a id="guidelines"></a>
## Usage Guidelines

The following describes the suggested uses and limitations of the vSWIM model. It follows a rough standard AI model reporting in model card format (see [Mitchell et al., 2015](https://dl.acm.org/doi/10.1145/3287560.3287596)). A more extensive overview can be found within the associated [publication](#citation)).

[1. Model Description](#model)
   
[2. Assessment](#assessment)

[3. Suggested Use Cases](#usecases)

[4. Limitations](#limits)
 


<a id="model"></a>
### 1. Model Description

#### Overview

- This model uses solar wind data measured from the MAVEN spacecraft since late 2014 and Gaussian process regression to generate continuous predictions (mean, $\mu$ and standard deviation, $\sigma$) of mulitple features of the solar wind including: 

   - IMF: $B_{x}$, $B_{y}$, $B_{z}$, and $|B|$ in [nT]
   - Velocity: $V_{x}$, $V_{y}$, $V_{z}$, and $|V|$ in [km/s]
   - Temperature: $T_{p}$ in [eV]
   - Pressure: $n_{p}$ in [per cc]

- All vector quanties are measured in Mars Solar Orbital (MSO) coordinates.

#### Data sources

- The original data used in for this process is from a combined SWIA and MAG (MAVEN instruments) data source, see [Halekas+2017](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016JA023167), [Halekas+2015](https://link.springer.com/article/10.1007/s11214-013-0029-z), [Connerney+2015](https://link.springer.com/article/10.1007/s11214-015-0169-4) and [online](https://homepage.physics.uiowa.edu/~jhalekas/drivers.html) for original data.</details>

#### Implementation

- We treat each feature seperately and discretize the entire dataset into subsets of 1,000 points before running a Gaussian process regression in [GPFlow](https://gpflow.github.io/GPflow/2.9.0/index.html). 
   
- y (solar wind feature) outputs are normalized to their mean and standard deviation of the subset, x (time) is normalized between 0 and 100. 

- We use a zero mean function and a [RationalQuadratic](https://gpflow.github.io/GPflow/develop/api/gpflow/kernels/index.html) covariance function kernel with:
    - l initialized to 0.1 of the non zero gaps betwen the dataset and ranging from the minimum to the median of the non zero gaps
    - the variance intitially set to 3.

- A fuller discussion of implementation Gaussian processes can be found within the [publication](#citation).


#### Example Algorithm
   - Split MAVEN dataset into 1000 datapoint subsets.
   - For each subset; and
        - For each feature in the dataset with $X^{j}$ being time, $y_{i}^{j}$ where i ranges from {0, 1, ..., 9}, corresponding to each solar wind feature and j ranges from {0, 1, ..., n} where n = 1000, the number of samples:
           - Normalize inputs
           - Initialize kernel hyperparameters
           - Run Gaussian process regression
           - Return predictions and unnormalize
 
<a id="asssessment"></a>
### 2. Assessment 
 
#### Test Set

- Poor model performance is a function of distance to a true (spacecraft measured) value. The test set then was designed to have the same distribution of data gaps as a final predicted proxy sampled at an hour cadence. All the following performance estimates are based on this test dataset.
   
#### Performance of Mean Prediction, $\mu$

- The performance of the mean predicted solar wind parameters (all) is the best when close to a real measurement.
- For an hourly cadence of prediction the estimated $R^{2}$ value is:
   - $\ge$ 0.95 within 2 days of a true measurement, this represents using roughly 66% of the dataset.
   - $\ge$ 0.62 within 10 days of a true measurement, this represents using roughly 80% of the dataset.
   - $\ge$ 0.48 within 28 days of a true measurement, this represents using roughly 95% of the dataset.
  
-  There are minor differences depending on the paramters in question with $V_{y}$ representing the poorest performing parameter.
-  It is worth noting that at large times from a true spacecraft measurement, the model can (and does) produce our initial 'guess' at the parameter value. From our initialization this is the mean value of the true dataset. You can identify when this occurs by reviewing the unnormalized prediction of $\mu$. When the unnormalized prediction of $\mu$ is close to 0, the prediction is the same as the initial subset's mean. 
  
#### Performance of Standard Deviation Prediction, $\sigma$

- One of the main purposes of this model is for uncertainty quantification. Every prediction $\mu$, has an associated $\sigma$ or predicted standard deviation.
- In the ideal case $\sigma$ should be representative of the true (or actual) model, and data, uncertainty.
- We estimated if $\sigma$ is capturing this uncertainty by evaluating the normalized residuals ($y_{model} - y_{data} / \sigma_{model}$).  
- We found that the uncertainties are:
   - unbiased, and accurate within 2 days of a true measurement, this represents using roughly 66% of the dataset.
   - unbiased, and mostly accurate (depends on the feature) within 10 days of a true measurement, this represents using roughly 80% of the dataset.
   - unbiased, and underestimated (scale depending on the feature) within 28 days of a true measurement, this represents using roughly 95% of the dataset.
- Full data can be found in the table within the associated [publication](#citation). 

 
  <a id="usecases"></a>
 ### 3. Suggested Use Cases

 - The most appropriate use case of this proxy is for large (multi-year) studies of Mars' space environment, ionosphere, and atmosphere or of general trends throughout the heliosphere.
 - Due to the nature of this prediction, $\sigma$ predictions should always be used with $\mu$ predictions. 
   
  <a id="limits"></a>
 ### 4. Limitations
 
 - This proxy does not capture short scale dynamic events (e.g. CMEs) or outliers unless the proxy itself is being used when MAVEN had solar wind data. Under this exception the proxy will roughly agree with the MAVEN data itself.
 - Vector quantiies are not guranteed to add in quadrature. Care should be taken when comparing components to magntitude predictions.
 - When this proxy is at 'its worst' (a long time since a recent measurement) the predicted value will be the mean of the subset of data. For certain parameters this is a poor representation of outliers.
 - Performance estimates are based on cumulative distributions (e.g. all predictions within 2 days, all predictions within 10 days, which includes predictions within 2 days). Performance for estimates between 8 and 10 days from a recent measurement is not the same as the estimate reported for all day within 10 days. 

