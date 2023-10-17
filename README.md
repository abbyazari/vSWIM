# vSWUM
A virtual solar wind upstream monitor (vSWUM) for planetary heliophysics with machine learning and spacecraft data.

This project is currently (10/17/2023) using data from the MAVEN mission and Gaussian process regression to estimate the upstream conditions at Mars.


Current issues (room for improvement): 

- Jasper's files are TOO LARGE to have hosted on Github in any way shape or form, we need data hosting of some sort somewhere along the path
- Same with orbital cadence of MAVEN, too large
- There are two paths:
1. Path 1: People have to grab their own files(?) and then run the code (this is probably the best option because this will be the smallest and fastest), This path would be heavily benefited from Jasper putting orbit numbers into his file that way people are not doing data merging on their home drives and we don't need to host files online or require the MAVEN toolkit. Abby Ask.
2. Path 2: We host the pickle files (somewhere?) and this repo just has the option to run the script itself that opens pickle files

Current inspo: https://sdoml.github.io/
