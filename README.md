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

   a. Overview: 
   
   This model uses solar wind data measured from the MAVEN spacecraft since late 2014 and Gaussian process regression to generate continuous predictions  
   (mean, $\mu$ and standard deviation, $\sigma$) of mulitple features of the solar wind including: $B_{x}$, $B_{y}$, $B_{z}$, $|B|$ in [nT], $V_{x}$,
   $V_{y}$, $V_{z}$, $|V|$ in [km/s], $T_{p}$ in [eV], and $n_{p}$ in [per cc]. All vector quanties are measured in Mars Solar Orbital (MSO) coordinates.
   
   b. Data sources: See [Halekas+2017](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016JA023167), [Halekas+2015](https://link.springer.com/article/10.1007/s11214-013-0029-z), [Connerney+2015](https://link.springer.com/article/10.1007/s11214-015-0169-4) and [online](https://homepage.physics.uiowa.edu/~jhalekas/drivers.html) for original data).
   
   c. Formulation:
   
   d. Data sources:
   
   e. Implementation: 
 
  <a id="asssessment"></a>
 ### 2. Assessment 
 
  <a id="usecases"></a>
 ### 3. Suggested Use Cases
 
  <a id="limits"></a>
 ### 4. Limitations
 
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
