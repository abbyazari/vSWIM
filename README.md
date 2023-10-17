# vSWUM
A virtual solar wind upstream monitor (vSWUM) for planetary heliophysics with machine learning and spacecraft data.

This project is currently (10/17/2023) using data from the MAVEN mission and Gaussian process regression to estimate the upstream conditions at Mars.


Current issues that are precluding Git progress: 

- Jasper's files (upstream original dataset) are TOO LARGE to have hosted on Github. 
- Same with orbital cadence of MAVEN, too large
- There are three paths:
1. Path 1: Write a 'grabber' that scraps Jaspers website when needed only for data that we want (regex).
2. Path 2: People have to grab their own files(?) and then run the code (this is probably the best option because this will be the smallest and fastest), This path would be heavily benefited from Jasper putting orbit numbers into his file that way people are not doing data merging on their home drives and we don't need to host files online or require the MAVEN toolkit.
3. Path 3: We host the pickle files (somewhere?) and this repo just has the option to run the script itself that opens pickle files

Current inspo: https://sdoml.github.io/
