# vSWIM<sup>beta</sup> - A Virtual Solar Wind Monitor for Mars 

### IMPORTANT: This repository is currently in beta and has been released for the peer review process (as of February 1, 2024). 

This reposiory consists of the source code to generate predictions of the upstream solar wind at Mars from [MAVEN](https://mars.nasa.gov/maven/) spacecraft data. 

### Contents

1. Hourly cadence solar wind predictions at [INSERT]. Use this if you need an [OMNI-like](https://omniweb.gsfc.nasa.gov/form/dx1.html) product at Mars.
2. Source code needed to generate predictions at [INSERT]. Use this if you need sub hour predictions of the solar wind at Mars.
3. A user guide for vSWIM. 

### User Guide

**Table of content:**
 - [Test](#item-one)
 
 <!-- headings -->
 <a id="item-one"></a>
 ### Hello World
 Hello world content goes here

The following describes the suggested uses and limitations of the vSWIM model. It follows a rough standard AI model reporting in model card format (see [Mitchell et al., 2015](https://dl.acm.org/doi/10.1145/3287560.3287596)). A more extensive overview can be found within [Azari et al., 2024](PENDING).

#### Model Description

Overview: This model is a Gaussian process regression on high-resolution upstream data from MAVEN SWIA and MAG from 2014 up to present.

Original data source: See [Halekas+2017](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016JA023167), [Halekas+2015](https://link.springer.com/article/10.1007/s11214-013-0029-z), [Connerney+2015](https://link.springer.com/article/10.1007/s11214-015-0169-4) and [online](https://homepage.physics.uiowa.edu/~jhalekas/drivers.html) for original data).

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
