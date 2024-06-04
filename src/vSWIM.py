#created by A. R. Azari on 2/1/2024
#see BSD-3 Liscense at https://github.com/abbyazari/vSWIM/blob/main/LICENSE.md
#see relevant materials at https://github.com/abbyazari/vSWIM/blob/main/Citation.bib 
#if using the original MAVEN generated data see https://github.com/abbyazari/vSWIM/tree/main
#for original data citations including but not limited to: 
#Halekas et al., 2017, Halekas et al., 2015, Connerney et al., 2015

#import required data grabbing and storing packages
import requests
import glob
import os
import regex                            as     re

#import GPU enabled GP packages
import tensorflow              as     tf
import tensorflow_probability  as     tfp
import gpflow

#import useful analysis
from   scipy.spatial.distance  import cdist
import pandas                  as     pd
import numpy                   as     np
import datetime                as     dt
from   sklearn.preprocessing   import StandardScaler, MinMaxScaler
import matplotlib.pyplot       as     plt

import argparse

#set random numbers for consistency between this run and 
#future use
rndm_no = 42
np.random.seed(rndm_no) #set numpy random seed
tf.random.set_seed(rndm_no)

#set global variable scaling constants for GP
maxRescale = 100
subsetSize = 1000
min_l      = 0.0 
mid_l      = 0.1
max_l      = 0.5
init_var   = 3

#full set of solar wind parameters
fullParams = ['b_x_SW',     'b_y_SW',    'b_z_SW',   'b_mag_SW',
              'v_x_SW',     'v_y_SW',    'v_z_SW',   'v_mag_SW', 
              'tp_SW',      'np_SW']


def getOrbitalData():
    
    '''
    Downloads MAVEN orbital ephemeris data from NASA SPICE. Optional, will only run if needing orbit numbers.
    '''

    baseURL = 'https://naif.jpl.nasa.gov/pub/naif/MAVEN/kernels/spk/'

    r = requests.get(baseURL)

    x = re.findall('"(maven_orb_rec_.*.orb)"', r.text)

    x.sort()

    orbs     = np.zeros(0)
    apoDates = np.zeros(0)


    for link in x:

        r = requests.get(baseURL+link)

        for line in r.text.splitlines()[2:]:

            orb = line.split()[0]

            dateStr = line.split()[6] + line.split()[7]  + line.split()[8]  + '-' + line.split()[9]

            apoDate = dt.datetime.strptime(dateStr, "%Y%b%d-%H:%M:%S")

            orbs = np.append(orbs, np.int32(orb))

            apoDates = np.append(apoDates, apoDate)
            
    return(orbs, apoDates)



def getMAVENData(saveMAVENData = False):
    
    '''
    Downloads data from Jasper Halekas' merged data product online at:
    https://homepage.physics.uiowa.edu/~jhalekas/drivers/drivers_merge_l2_hires.txt

    See Halekas et al., 2017 for relevant information on the original merged product. 

    See Halekas et al., 2015, Connerney et al. 2015 for original instrument papers.
    
    Defaults to not saving file on local drive. 
    
    If save file is enabled, will save to ./Data/drivers_merge_l2_hires.txt on local file
    diretory. 
    '''

    mav_file = 'https://homepage.physics.uiowa.edu/~jhalekas/drivers/drivers_merge_l2_hires.txt'

    #read in Halekas file (direct measurements)
    colNames = ['date', 'np_SW', 'nalpha_SW', 'v_SW', 
                'v_x_SW', 'v_y_SW', 'v_z_SW', 'tp_SW', 
                'b_x_SW', 'b_y_SW', 'b_z_SW']

    maven = pd.read_csv(mav_file, names = colNames, index_col = False, sep = r'\s+')
    

    maven['date_SW'] = pd.to_datetime(maven['date'])

    maven['date_SW_unix'] = (maven['date_SW'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    maven['b_mag_SW'] = np.sqrt(maven.b_x_SW**2.0 + maven.b_y_SW**2.0 + maven.b_z_SW**2.0)

    maven['v_mag_SW'] = np.sqrt(maven.v_x_SW**2.0 + maven.v_y_SW**2.0 + maven.v_z_SW**2.0)
    
    if saveMAVENData:

        locResults = './results/'

        try:
            os.mkdir(locResults)
        
        except:
          #if directory already exists do nothing  
          pass

        print("Saving data from https://homepage.physics.uiowa.edu/~jhalekas/drivers.html, see Halekas et al., 2017 to {}.".format(locResults))
        
        maven.to_csv('{}halekas2017_drivers_merge_l2_hires.csv'.format(locResults))

    #smallest number of subsets, only count full subsets 
    
    numSubsets = int(len(maven) / subsetSize)

    maven['SubsetIndex'] = np.nan

    for i in np.arange(0, numSubsets):

        maven.loc[i * subsetSize : i * subsetSize + subsetSize - 1, 'SubsetIndex'] = i
    
    return(maven)
    

def runvSWIM(startDate = dt.datetime(2015, 1,  1), stopDate  = dt.datetime(2015, 1,  4), cadence = 60*60, 
             params = ['b_x_SW',     'b_y_SW',    'b_z_SW',   'b_mag_SW',
                        'v_x_SW',    'v_y_SW',    'v_z_SW',   'v_mag_SW', 
                        'tp_SW',      'np_SW'],    
             getOrb = False, saveModelResults = False, saveMAVENData = False, returnOriginal = False, verbose = False):
    
    '''
    Run the vSWIM model over a set period of time at a cadence in seconds. 
    
    If you want to save a copy of the original MAVEN file to the Data folder
    use saveMAVENData = True.
    
    If you want to save the results of the model to the Data folder
    use saveModelResults = True.
    
    You can run any of the following parameters: b_x_SW, b_y_SW, b_z_SW, b_mag_SW,
                                                 v_x_SW, v_y_SW, v_z_SW, v_mag_SW, 
                                                 tp_SW,  np_SW
                                                 
    Note 1: future improvements will have user input checks.
    
    Note 2: this function can not be run before dt.datetime(2014, 11, 12, 12).
    
    '''
    #check user inputs
    if ((type(startDate)  != type(dt.datetime(2015, 1, 1))) | 
             ((type(stopDate) != type(dt.datetime(2015, 1, 1))))):
        raise TypeError('Check time range type, use dt.datetime format.')
    
    if (type(params) != type(['a', 'b'])):
        raise ValueError("Check solar wind entry parameter type, use ['param1', 'param2'] format.")
        
    #check if user used a real solar wind parameter and correct time range.
    if (startDate >= stopDate):
        raise ValueError("Can not run on stopDate <= startDate.")
    
    for p_i in params:
        if not p_i in fullParams:           
            raise ValueError('{} is not within valid solar wind options: {}'.format(p_i, fullParams))
                
    #read in maven if passed checks
    print("Reading in original MAVEN files.")
    maven = getMAVENData(saveMAVENData)
    
    #check if user picked a valid date of MAVEN
    if ((startDate < pd.to_datetime(maven[::subsetSize].date_SW.values[0])) | 
        (stopDate  > pd.to_datetime(maven[::subsetSize].date_SW.values[-2]))):
        raise ValueError('Can only run from {} to {}, pick new time range.'.format(
                                        pd.to_datetime(maven[::subsetSize].date_SW.values[0]),
                                        pd.to_datetime(maven[::subsetSize].date_SW.values[-2])))
    
    startSubsets = maven[::subsetSize]

    indexStart = startSubsets.loc[startSubsets['date_SW'] <= startDate, 'SubsetIndex'].values[-1]
    indexStop  = startSubsets.loc[startSubsets['date_SW'] >= stopDate,  'SubsetIndex'].values[0]

    results = pd.DataFrame()

    results['date_[utc]']  = pd.to_datetime(np.arange(startDate, stopDate, 
                                                        dt.timedelta(seconds = cadence)))

    results['date_[unix]']  = ((results['date_[utc]'] - pd.Timestamp("1970-01-01")) //
                                pd.Timedelta('1s'))


    results['gap']      = np.nan

    if getOrb:
        
        print('Generating MAVEN orbit information.')

        results['orb']          = np.nan

        orbs, apoDates = getOrbitalData()

        orbStart = orbs[(apoDates >= results['date_[utc]'][0])][0] - 1 
        orbStop  = orbs[(apoDates <  results['date_[utc]'][len(results) - 1])][-1] 


        for orb in np.arange(orbStart, orbStop + 1):


            index = (orbs == orb)

            startApo = apoDates[orbs == orb][0] 
            endApo   = apoDates[orbs == orb + 1][0]

            orbIndex = ((results['date_[utc]'] >= startApo) & (results['date_[utc]'] < endApo))

            results.loc[orbIndex, 'orb'] = orb

    print('Running from {} to {}, in {} segments, and for parameters:'.format(startDate, 
                                                                              stopDate, 
                                                                              indexStop - indexStart))

    for p in params:

        print('{}'.format(p))

        results['mu_{}'.format(p)]            = np.nan

        results['sigma_{}'.format(p)]         = np.nan

        results['mu_{}_normed'.format(p)]     = np.nan

        results['sigma_{}_normed'.format(p)]  = np.nan


    
    arrEnum  = np.arange(indexStart, indexStop, 1)
    
    for i, o in enumerate(arrEnum):


        #if short, print everyone
        if len(arrEnum) < 10:
            
            print('\nOn {} / {} segments'.format(i + 1, len(arrEnum)))

        #if long, print every 5
        else:
            
            if ((i % 5) == 0):

                print('\nOn {} / {} segments'.format(i + 1, len(arrEnum)))

        data = maven[maven[maven.SubsetIndex == o].index[0]:maven[maven.SubsetIndex == o + 1].index[1]]


        indResults = ((results['date_[utc]'] >= data.date_SW.values[0]) & 
                        (results['date_[utc]'] < data.date_SW.values[-1]))



        X_train = data['date_SW_unix'].values.reshape(-1, 1) 


        results.loc[indResults, 'gap'] = np.around(np.min(cdist(results.loc[indResults, 
                                                                'date_[unix]'].values.reshape(-1, 1),
                                                    data.date_SW_unix.values.reshape(-1, 1)), 1) / (60*60*24),
                                                    decimals = 3)

        for p in params:

            if verbose:
                print(p)

            y_train = data['{}'.format(p)].values.reshape(-1, 1)


            normScaler = StandardScaler()

            normScaler.fit(y_train)

            mmScaler = MinMaxScaler(feature_range=(0, maxRescale))
            mmScaler.fit(X_train)

            X_normed_train = mmScaler.transform(X_train)
            y_normed_train = normScaler.transform(y_train)

            dists        = cdist(X_normed_train, X_normed_train)

            dists_noZeros = dists[dists != 0]

            minLength = np.quantile(dists_noZeros, min_l)

            midLength = np.quantile(dists_noZeros, mid_l)

            maxLength = np.quantile(dists_noZeros, max_l)


            signal_kernel = gpflow.kernels.RationalQuadratic(variance = init_var)


            signal_kernel.lengthscales = gpflow.Parameter(midLength, 
                                    transform=tfp.bijectors.SoftClip(
                                        gpflow.utilities.to_default_float(minLength),
                                        gpflow.utilities.to_default_float(maxLength)))


            model = gpflow.models.GPR((X_normed_train, y_normed_train), kernel=signal_kernel)

            opt = gpflow.optimizers.Scipy()

            opt.minimize(model.training_loss, model.trainable_variables)

            if verbose: 
                gpflow.utilities.print_summary(model, "notebook")

            #----------and now save results


            X_model = mmScaler.transform(results.loc[indResults, 'date_[unix]'].values.reshape(-1, 1))

            mean_model, var_model = model.predict_y(X_model)
            mean_model = np.array(mean_model)
            var_model = np.array(var_model)

            std_model = np.sqrt(var_model)

            results.loc[indResults, 'mu_{}_normed'.format(p)]    = mean_model

            results.loc[indResults, 'sigma_{}_normed'.format(p)] = std_model

            mean_model_unnorm = normScaler.inverse_transform(mean_model.reshape(-1, 1))[:, 0]

            std_model_unnorm  = std_model*normScaler.scale_

            results.loc[indResults, 'mu_{}'.format(p)]    = mean_model_unnorm

            results.loc[indResults, 'sigma_{}'.format(p)] = std_model_unnorm

    if saveModelResults:

        #make directory

        locResults = './results/'

        try:
            os.mkdir(locResults)
        
        except:
          #if directory already exists do nothing  
          pass
          

        print('\nSaving model outputs to {}'.format(locResults))
        
        results.to_csv('{}vSWIM_{:%Y-%m-%d:%H-%M-%S}_{:%Y-%m-%d:%H-%M-%S}.csv'.format(locResults, startDate, stopDate))

    if returnOriginal: 
        
        return(maven, results)

    else:
        return(results)

if __name__ == "__main__":
    
        
    #add command line functionality
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--start_date", type=dt.datetime.fromisoformat, default="2015-01-01", help="start date in any ISO format")
    parser.add_argument("--end_date", type=dt.datetime.fromisoformat, default="2015-01-04", help="start date in any ISO format")
    parser.add_argument("--cadence", type=int, default=1, help="interpolation cadence in seconds")
    parser.add_argument("--params_list", type=str, nargs='+', default = ['v_x_SW'], help="solar wind parameters to interpolate, "+\
                                                                                         "list any of:  b_x_SW, b_y_SW, b_z_SW, b_mag_SW, "+\
                                                                                         "v_x_SW, v_y_SW, v_z_SW, v_mag_SW, tp_SW,  np_SW" )

    parser.add_argument("--get_orb", action="store_false", help="include orbital information")
    parser.add_argument("--save_model_results", action="store_false", help="save model results to csv in the data folder")
    parser.add_argument("--save_maven_data", action="store_false", help="save a copy of the original MAVEN data in the data folder")
    parser.add_argument("--return_original", action="store_false", help="returns a copy of the original MAVEN data to user")
    parser.add_argument("--verbose", action="store_false", help="increase output verbosity")
    
    args = parser.parse_args()
