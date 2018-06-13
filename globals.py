#Technical parameters
SAMPLE_RELIABILITY_EXPONENTS = range(-2,11)
#sampleReliabilities = 1-np.divide(0.1,np.power(2.,sampleReliabilityExponents))
DEFAULT_PEAK_CAPACITY = 2 #kW
DEFAULT_DAILY_LOAD = 8.2 #kw/day
DEFAULT_SOLAR_DERATE = 85 #percent
DEFAULT_BATTERY_LIFETIME = 10 #years

#Economic parameters
DEFAULT_CURRENCY = 'USD'
DEFAULT_BATTERY_COST = 400 #$/kWh
DEFAULT_SOLAR_COST = 1000 #$/kW
DEFAULT_CHARGE_CONTROLLER_COST = 200 #$/kW
DEFAULT_CAPACITY_COST = 1300 #$/kW of peak load rest
DEFAULT_FIXED_COST = 0 #$
DEFAULT_OM_FACTOR = 5 #(%)
DEFAULT_TERM = 20 #years
DEFAULT_DISCOUNT_RATE= 10 #per year

#Miscellaneous
MAPBOX_TOKEN = 'pk.eyJ1IjoibGVlanQ0ODkiLCJhIjoiY2ppZGlwdmM2MGJ5eDNxcXYyYXM2anM2eiJ9.GZIpHlXBzxcJFZlacUxIoQ'
DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", \
	"#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", \
	"#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]
