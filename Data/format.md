
# Format Information for Hour Resolution Files 

###*IMPORTANT: Please refer to [user guidelines](https://github.com/abbyazari/vSWIM/edit/main/) for user information before using these data.

## Directory Structure

- Files are organized as YYYY-YYYY_Hourly.csv for all years that real time data was observed from the MAVEN mission. These files will continue to be updated as the mission progresses.
- Files are located at https://github.com/abbyazari/vSWIM/tree/main/Data.

## File Content

- Predictions every hour are provided in these files of the following parameters:
  - IMF: $B_{x}$, $B_{y}$, $B_{z}$, and $|B|$ in [nT]
  - Velocity: $V_{x}$, $V_{y}$, $V_{z}$, and $|V|$ in [km/s]
  - Temperature: $T_{p}$ in [eV]
  - Pressure: $n_{p}$ in [per cc]
- These parameters are provided with a mean value and a standard deviation for both the true and the normalized values. The normalized values are provided as optional additional information to assess when model performance (see [user guide](https://github.com/abbyazari/vSWIM/edit/main/)). The naming convention is as follows: 
  - mean, mu_paramName
  - standard deviation, sigma_paramName
  - mean normalized, mu_paramName_normed
  - stadard deviation normalized, sigma_paramName_normed
- Additional values are provided including:
  - date [utc], the date in UTC
  - date [unix], the date in UNIX 
  - gap, the time in days to a recent MAVEN measurement
  - orb, the MAVEN orbit number 


