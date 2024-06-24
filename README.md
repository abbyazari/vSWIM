# vSWIM - A Virtual Solar Wind Monitor for Mars 

[![DOI](https://zenodo.org/badge/706391083.svg)](https://zenodo.org/doi/10.5281/zenodo.11106970)

This repository contains predictions of the solar wind upstream of Mars from late 2014 onwards as calculated with a predictive model and [MAVEN](https://mars.nasa.gov/maven/) spacecraft data. This model output is useful for statistical studies where a continuous estimation of the solar wind at Mars with uncertainties is needed. Future iterations are expected that include solar wind observations from other missions to Mars.

We highly recommend that users review the brief usage guidelines below before using either the model or the associated predictions. 

## Contents

1. **Low Resolution Data:** Hourly cadence solar wind [predictions](https://github.com/abbyazari/vSWIM/edit/main/data). Use this if you need an [OMNI-like](https://omniweb.gsfc.nasa.gov/form/dx1.html) product. A human readable data format description is also [provided](https://github.com/abbyazari/vSWIM/blob/main/data/format.md).
2. **Model:** [Source code](https://github.com/abbyazari/vSWIM/edit/main/src) needed to generate predictions. Use this if you need sub hour predictions of the solar wind at Mars.
3. **Usage Guidelines:** A short [user guide](#guidelines) for vSWIM. Read this if you need to use either 1 or 2.
4. **Tutorials:** Short [tutorials](https://github.com/abbyazari/vSWIM/tree/main/) for reading the data or running the model.



<a id="citation"></a>
## Citing vSWIM

If you use this product please reference the submitted [JGR Machine Learning paper](https://arxiv.org/abs/2402.01932). Sample Bibtex is given below. Please additionally see relevant citations for the current source datasets under the model [description](#model).

```
@article{Azari2024,
author = {Azari, A. R. and Abrahams, E. and Sapienza, F. and Halekas, J. and Biersteker, J. and 
Mitchell, D. L. and Pérez, F. and Marquette, M. and Rutala, M. J. and Bowers, C. F. and 
Jackman, C. M. and Curry, S. M.},
eprint={2402.01932},
journal = {Accepted to the Journal of Geophysical Research: Machine Learning and Computation},
title = {A Virtual Solar Wind Monitor at {M}ars with Uncertainty Quantification using
{G}aussian Processes},
year = {2024},
url  = {https://arxiv.org/abs/2402.01932}
}
```

 <!-- headings -->
 <a id="guidelines"></a>
## Usage Guidelines

The following describes the suggested uses and limitations of the vSWIM model. It follows a rough standard AI model reporting in model card format (see [Mitchell et al., 2015](https://dl.acm.org/doi/10.1145/3287560.3287596)). A more extensive overview can be found within the associated [publication](#citation).

[1. Model Description](#model)

[2. Installation](#install)
   
[3. Assessment](#assessment)

[4. Suggested Use Cases](#usecases)

[5. Limitations](#limits)
 


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

- The dataset(s) used in the current iteration of this model are from a combined SWIA and MAG (MAVEN instruments) data source, see [Halekas+2017](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016JA023167), [Halekas+2015](https://link.springer.com/article/10.1007/s11214-013-0029-z), [Connerney+2015](https://link.springer.com/article/10.1007/s11214-015-0169-4) and [online](https://homepage.physics.uiowa.edu/~jhalekas/drivers.html) for original data. Sample bibtex of relevant data sources is given below.

- For the integrated MAVEN dataset:

```
@article{Halekas2017,
author = {Halekas, J. S. and Ruhunusiri, S. and Harada, Y. and Collinson, G. and Mitchell, D. L. and
Mazelle, C. and McFadden, J. P. and Connerney, J. E. P. and Espley, J. R. and Eparvier, F. and
Luhmann, J. G. and Jakosky, B. M.},
title = {Structure, dynamics, and seasonal variability of the {M}ars-solar wind interaction:
{MAVEN Solar Wind Ion Analyzer} in-flight performance and science results},
journal = {Journal of Geophysical Research: Space Physics},
volume = {122},
number = {1},
pages = {547-578},
doi = {10.1002/2016JA023167},
year = {2017}
}
```

- For the MAVEN SWIA instrument:
```
@article{Halekas2015,
author = {Halekas, J. S. and Taylor, E. R. and Dalton, G. and Johnson, G. and Curtis, D. W.
and McFadden, J. P. and Mitchell, D. L. and Lin, R. P. and Jakosky, B. M.},
title = {{The Solar Wind Ion Analyzer for MAVEN}},
journal = {Space Science Reviews},
volume = {195},
number = {1},
pages = {125-151},
doi = {10.1007/s11214-013-0029-z},
year = {2015}
}
```

- For the MAVEN MAG instrument:

```
@article{Connerney2015,
author = {Connerney, J. E. P. and Espley, J. and Lawton, P. and Murphy, S. and Odom, J. and
Oliversen, R. and Sheppard, D.},
title = {{The MAVEN Magnetic Field Investigation}},
journal = {Space Science Reviews},
volume = {195},
number = {1},
pages = {257-291},
doi = {10.1007/s11214-015-0169-4},
year = {2015}
}
```



#### Implementation

- We treat each feature seperately and discretize the entire dataset into subsets of 1,000 points before running a Gaussian process regression in [GPFlow](https://gpflow.github.io/GPflow/2.9.0/index.html). 
   
- y (solar wind feature) outputs are normalized to their mean and standard deviation of the subset, x (time) is normalized between 0 and 100. 

- We use a zero mean function and a [RationalQuadratic](https://gpflow.github.io/GPflow/develop/api/gpflow/kernels/index.html) covariance function kernel with:
    - l initialized to 0.1 of the non zero gaps betwen the dataset and ranging from the minimum to the median of the non zero gaps,
    - the variance intitially set to 3.

- A fuller discussion of Gaussian processes can be found within the [publication](#citation).


#### Example Algorithm
   - Split MAVEN dataset into subsets of 1000 datapoints each.
   - For each subset; and
        - For each feature in the dataset with $X^{j}$ being time, $y_{i}^{j}$ where i ranges from {0, 1, ..., 9}, corresponding to each solar wind feature and j ranges from {0, 1, ..., n} where n = 1000, the number of samples:
           - Normalize inputs
           - Initialize kernel hyperparameters
           - Run Gaussian process regression
           - Return predictions and unnormalize

<a id="install"></a>
### 2. Installation 

Option 1 (recommended): You can run this model by:
- (1) install Python (v3.12) 
- (2) download this repository 
- (3) create a virtual environment
- (4) run pip install -r requirements.txt (or use conda)
- (5) check installation by following tutorials or run via Python (from src import vSWIM, predictions = vSWIM.runvSWIM())

Option 2: Alternatively if you prefer to manage your own Python environment directly the primary package needed is GPFlow which has dependencies on TensorFlow and TensorFlow Probability. while most other packages (e.g. pandas, numpy) you likely have in your current Python set up, you will need to install TensorFlow, TensorFlow Probability, and GPFlow. We recommend you use the GPFlow installation [guide](https://github.com/GPflow/GPflow?tab=readme-ov-file#installation).

Note, you only need these installations if you plan on using the full model. The hourly [predictions](https://github.com/abbyazari/vSWIM/edit/main/data) do not require this installation.  

<a id="asssessment"></a>
### 3. Assessment 
 
#### Test Set

- Model performance is a function of distance to a true (spacecraft measured) value. The test set then was designed to have the same distribution of data gaps as a final predicted proxy sampled at an hour cadence. All the following performance estimates are based on this test dataset.
   
#### Performance of Mean Prediction, $\mu$

- The performance of the mean predicted solar wind parameters (all) is the best when close to a real measurement.
- For an hourly cadence of prediction the estimated $R^{2}$ value is:
   - $\ge$ 0.95 within 2 days of a true measurement, this represents using roughly 66% of the dataset.
   - $\ge$ 0.62 within 10 days of a true measurement, this represents using roughly 80% of the dataset.
   - $\ge$ 0.48 within 28 days of a true measurement, this represents using roughly 95% of the dataset.
  
-  There are minor differences depending on the paramters in question with $V_{y}$ representing the poorest performing parameter.
-  It is worth noting that at large times from a true spacecraft measurement, the model can (and does) produce our initial 'guess' at the parameter value. From our initialization this is the mean value of a subsset of the true dataset. You can identify when this occurs by reviewing the unnormalized prediction of $\mu$. When the unnormalized prediction of $\mu$ is close to 0, the prediction is the same as the initial subset's mean. 
  
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
 ### 4. Suggested Use Cases and Tips

 - The most appropriate use cases of this proxy are for large (multi-year) studies of Mars' space environment, ionosphere, and atmosphere or of general trends throughout the heliosphere.
 - Due to the nature of this prediction, $\sigma$ predictions should always be used with $\mu$ predictions.
 - If you are using the hourly prediction, you can read these files *directly* into a Pandas dataframe without downloading the original file to your local machine with pd.read_csv.
 - If you are using this proxy for an event study (i.e. not a multi-year study) please read the limitations section below and consider using the original mission [datasets](#model) instead of this product.

 - The following example is provided for reading the hourly datafiles, see [tutorial #1](https://github.com/abbyazari/vSWIM/blob/main/readDataTutorial.ipynb) for more information:

```
 #Read the hourly predictions into a Pandas dataframe: 
 
 data = pd.read_csv('https://raw.githubusercontent.com/abbyazari/vSWIM/main/data/YYYY-YYYY_Hourly.csv',
                     index_col=['Unnamed: 0'])

```

 - The following example is provided for running the model directly, see [tutorial #2](https://github.com/abbyazari/vSWIM/blob/main/runModelTutorial.ipynb) for more information:

```
 #Run the model with default key word arguments: 
 
 maven, results  = vSWIM.runvSWIM()

```

 - If you are using IDL see helpful function created by K. G. Hanley which converts the output .csv to .sav files at [./src/IDLTools](https://github.com/abbyazari/vSWIM/tree/main/src/IDLTools) 

  <a id="limits"></a>
 ### 5. Limitations
 
 - This proxy does not capture short scale dynamic events (e.g. CMEs) or outliers unless the proxy itself is being used when MAVEN had solar wind data. Under this exception the proxy will roughly agree with the MAVEN data itself. If interested in the directly measured solar wind with no continuous estimation as provided by this model, please use the the uninterpolated mission [datasets](#model).
 - Vector quantiies are not guaranteed to add in quadrature. Care should be taken when comparing components to magntitude predictions.
 - When this proxy is at 'its worst' (a long time since a recent measurement) the predicted value will be the mean of the subset of data. For certain parameters this is a poor representation of outliers. This can be filtered via restricting to a reasonable time to a recent measurement (the 'gap' column). See data [format](https://github.com/abbyazari/vSWIM/blob/main/data/format.md) information.
 - Performance estimates in the associated paper are based on cumulative distributions (e.g. all predictions within 2 days, all predictions within 10 days, which includes predictions within 2 days). Performance for estimates between 8 and 10 days from a recent measurement is not the same as the estimate reported for all day within 10 days. As a result, we do not recommend this proxy is used for event studies that are limited to only data (e.g. only 2-4 days, only 8-10 days etc) that is far from a recent measurement. 
 - We do not reccomend upsampling (interpolating) hourly predictions to a lower time cadence, instead we direct users to running the model directly at the time cadence they desire.
 - Downsampling to lower time resolutions (i.e. 10 hour predictions from the 1 hour files) is a reasonable use of this model. 

## Funding

This project has been supported by:
- The MAVEN mission project; via NASA through the Mars Exploration Program and by grant NNH10CC04C to the University of Colorado and subsequent subcontract to Space Sciences Laboratory, University of California, Berkeley.
- NASA’s AI / ML Use Case Program, grant 80NSSC21K1370. 
- Computation was enabled by the NSF Earth Cube Program under awards 1928406, 1928374. 
- The lead developer is currently supported by the Data Science Fellowship at the University of British Columbia through the Data Science Institute’s Postdoctoral Matching Fund.

