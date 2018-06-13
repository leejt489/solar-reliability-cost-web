topText= '''
## Welcome!
This is a tool for estimating the cost of standalone, or "off-grid", solar-plus-storage systems, with a specific emphasis on reliability. We use the fraction of demand served (FDS) as a reliability metric, which measures the ratio of energy supplied to energy demanded over a time period. A full description of methods used to estimate the cost is described in the [Nature Energy article]() found at [ADDRESS](). In essence, you can adjust the technical and economic parameters below and click the "Update Map" button to see the spatial variation in the levelized cost of energy. Given the parameters, the program computes the cost-minimizing system using 11 years of daily solar irradiance provided by [NASA's Surface meteorology and Solar Energy database](https://eosweb.larc.nasa.gov/sse/).

The creators of this tool request that users consult and provide attribution to the following article for all academic research using this tool:

Lee, Jonathan and Callaway, Duncan. The cost of reliability in decentralized solar power systems in sub-Saharan Africa. *Nature Energy*, (Under Review).

Please file issues, bugs, and feature requests for the tool on [GitHub](https://github.com/leejt489/solar-reliability-cost-web/issues). You can also view the code for the underlying optimization in [MATLAB](https://github.com/leejt489/solar-reliability-cost-matlab) and in [Python 3](https://github.com/leejt489/solar-reliability-cost-python), and can use those repositories to file issues there as well.
'''
