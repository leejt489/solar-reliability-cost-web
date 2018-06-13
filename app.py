import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import numpy as np
import json


app = dash.Dash(__name__)
server = app.server
#app.scripts.config.serve_locally=True
app.css.append_css({
    #'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'
})
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/dZVMbK.css"})

DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", \
	"#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", \
	"#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]

colorscale = DEFAULT_COLORSCALE

mapboxToken = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2oyY2M4YW55MDF1YjMzbzhmemIzb290NiJ9.sT6pncHLXLgytVEj21q43A'

reliabilityFrontiers = json.load(open('reliabilityFrontiers_constant_africa_1.json'))

#Technical parameters
sampleReliabilityExponents = np.arange(-2,11)
#sampleReliabilities = 1-np.divide(0.1,np.power(2.,sampleReliabilityExponents))
getReliabilityValue = lambda r: 1-0.1/(2.**r)
DEFAULT_DAILY_LOAD = 8.2 # kWh/day
DEFAULT_PEAK_CAPACITY = 2 #kW
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

parameterSectionTechnicalItems=[
    html.H3('Technical'),
    html.Hr(),
    html.Div(
        className='row col-sm-12',
        children=[
            html.Label('Target reliability (Fraction of Demand Served)'),
            html.Div(children=[dcc.Slider(
                id='sliderReliability',
                min=sampleReliabilityExponents[0],
                max=sampleReliabilityExponents[-1],
                value=3,
                step=1,
                marks={str(r): '{:0.2f}'.format(getReliabilityValue(r)*100) for r in [-2,0,3,7,10]}
            )],style={'padding-bottom':20,'padding-left':10,'padding-right':10}),
            html.Div(id='dispReliabilityValue')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Daily Load (kWh/day)'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputDailyLoad',type='number',value=DEFAULT_DAILY_LOAD
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Peak Capacity (kW)'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputPeakCapacity',type='number',value=DEFAULT_PEAK_CAPACITY
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Solar Derating (%)'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputSolarDerate',type='number',value=DEFAULT_SOLAR_DERATE,
                    min=0,max=100
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Battery Lifetime (yrs)'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputBatteryLifetime',type='number',value=DEFAULT_BATTERY_LIFETIME
            ),className='col-lg-6')
        ]
    )
]

parameterSectionEconomicItems=[
    html.H3('Economic'),
    html.Hr(),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Currency'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputCurrency',type='text',value=DEFAULT_CURRENCY
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label(id='labelBatteryCost'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputBatteryCost',type='number',value=DEFAULT_BATTERY_COST
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label(id='labelSolarCost'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputSolarCost',type='number',value=DEFAULT_SOLAR_COST
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label(id='labelChargeControllerCost'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputChargeControllerCost',type='number',
                value=DEFAULT_CHARGE_CONTROLLER_COST
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label(id='labelCapacityCost'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputCapacityCost',type='number',value=DEFAULT_CAPACITY_COST
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label(id='labelFixedCost'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputFixedCost',type='number',value=DEFAULT_FIXED_COST
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Operations and Maintenance Factor (% of total capital cost)'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputOMFactor',type='number',value=DEFAULT_OM_FACTOR
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Project Term (yrs)'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputTerm',type='number',value=DEFAULT_TERM
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Discount Rate (%)'),className='col-lg-6'),
            html.Div(dcc.Input(
                id='inputDiscountRate',type='number',value=DEFAULT_DISCOUNT_RATE,
                    min=0,max=100
            ),className='col-lg-6')
        ]
    )
]

parameterSectionItems=[
    html.H2('Parameters'),
    html.Hr(),
    html.Button(id='buttonUpdateMap', n_clicks=0, children='Update Map'),
    html.Hr(),
    html.Div(
        className='row',
        children=[
            html.Div(
                children=parameterSectionTechnicalItems,
                className="col-md-6"
            ),
            html.Div(
                children=parameterSectionEconomicItems,
                className="col-md-6"
            )
        ]
    ),
    html.Hr(),
    html.Button(id='buttonUpdateMap2', children='Update Map')
]

app.layout = html.Div(
    className='container-fluid',
    children=[
        html.Div(
            className='row col-xs-12',
            children=[
                html.H1('[Under Construction]'),
                html.H1('Estimated Cost of Decentralized Solar Power Systems in sub-Saharan Africa'),
                html.Hr()
            ]
        ),
        html.Div(
            className='row col-xs-12',
            children=[
                dcc.Markdown('''
## Welcome!
This is a tool for estimating the cost of standalone, or "off-grid", solar-plus-storage systems, with a specific emphasis on reliability. We use the fraction of demand served (FDS) as a reliability metric, which measures the ratio of energy supplied to energy demanded over a time period. A full description of methods used to estimate the cost is described in the [Nature Energy article]() found at [ADDRESS](). In essence, you can adjust the technical and economic parameters below and click the "Update Map" button to see the spatial variation in the levelized cost of energy. Given the parameters, the program computes the cost-minimizing system using 11 years of daily solar irradiance provided by [NASA's Surface meteorology and Solar Energy database](https://eosweb.larc.nasa.gov/sse/).

The creators of this tool request that users consult and provide attribution to the following article for all academic research using this tool:

Lee, Jonathan and Callaway, Duncan. The cost of reliability in decentralized solar power systems in sub-Saharan Africa. *Nature Energy*, (Under Review).

Please file issues, bugs, and feature requests for the tool on [GitHub](https://github.com/leejt489/solar-reliability-cost-web/issues). You can also view the code for the underlying optimization in [MATLAB](https://github.com/leejt489/solar-reliability-cost-matlab) and in [Python 3](https://github.com/leejt489/solar-reliability-cost-python), and can use those repositories to file issues there as well.
                '''),
                html.Hr()
            ]
        ),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-md-6',
                    children=parameterSectionItems
                ),
                html.Div(
                    className='col-md-6',
                    children=[
                        html.H2('Map of levelized cost of electricity (LCOE)'),
                        dcc.Graph(
                            id='map',
                            #animate=True,
                            figure = {
                                'data': [],
                                'layout': {
                                    'mapbox': {
                                        'layers': [],
                                        'accesstoken': mapboxToken,
                                        'center': {
                                            'lat': 0,
                                            'lon': 20,
                                        },
                                        'zoom': 2,
                                        'pitch': 0
                                    }
                                }
                            })
                    ]
                )
            ]
        ),
        html.Hr(),
        html.Div(
            className='row col-xs-12',
            children=dcc.Markdown('&#169; Jonathan Lee, 2018')
        )
    ]
)

@app.callback(Output('dispReliabilityValue','children'),
    [Input('sliderReliability','value')])
def display_value(reliabilityExponent):
    return dcc.Markdown('Selected FDS: **{:0.2f}%**'.format(getReliabilityValue(reliabilityExponent)*100))

@app.callback(Output('labelBatteryCost','children'),
    [Input('inputCurrency','value')])
def display_value(text):
    return 'Battery Cost ({}/kWh)'.format(text)

@app.callback(Output('labelSolarCost','children'),
    [Input('inputCurrency','value')])
def display_value(text):
    return 'Solar Cost ({}/kW, including racking)'.format(text)

@app.callback(Output('labelChargeControllerCost','children'),
    [Input('inputCurrency','value')])
def display_value(text):
    return 'Charge Controller Cost ({}/kW)'.format(text)

@app.callback(Output('labelCapacityCost','children'),
    [Input('inputCurrency','value')])
def display_value(text):
    return 'Capacity Cost ({}/kW) - Includes inverter/DC power supply, balance-of-system, etc.; i.e. variable costs per peak capacity'.format(text)

@app.callback(Output('labelFixedCost','children'),
    [Input('inputCurrency','value')])
def display_value(text):
    return 'Additional Fixed Cost ({})'.format(text)


@app.callback(
    dash.dependencies.Output('map','figure'),
    [
        Input('buttonUpdateMap','n_clicks'),
        Input('buttonUpdateMap','n_clicks')
    ],
    [
        State('sliderReliability','value'),
        State('inputDailyLoad','value'),
        State('inputPeakCapacity','value'),
        State('inputSolarDerate','value'),
        State('inputBatteryLifetime','value'),
        State('inputBatteryCost','value'),
        State('inputSolarCost','value'),
        State('inputChargeControllerCost','value'),
        State('inputCapacityCost','value'),
        State('inputFixedCost','value'),
        State('inputOMFactor','value'),
        State('inputTerm','value'),
        State('inputDiscountRate','value'),
        State('inputCurrency','value'),
        State('map', 'figure')
    ]
)
def display_map(_,__,reliabilityExponent,dailyLoad,peakCapacity,solarDerate,
    batteryLifetime,storageCost,solarCost,chargeControllerCost,capacityCost,
    fixedCost,oAndMFactor,term,discountRate,currency,figure):

    #Convert percentage to per unit
    discountRate = discountRate/100
    solarDerate = solarDerate/100
    oAndMFactor = oAndMFactor/100
    reliability = getReliabilityValue(reliabilityExponent)

    solarTotalCost = solarCost/solarDerate+chargeControllerCost #Solar lifetime assumed to be term
    storageTotalCost = storageCost*(1-(1-discountRate)**term)/(1-(1-discountRate)**batteryLifetime) #Includes replacement cost of storage
    crf = (discountRate*(1+discountRate)**term)/(((1+discountRate)**term)-1)

    resolution = 1
    latArray = []
    lonArray = []
    LCOE = []
    hoverText = []

    rKey = '{:f}'.format(reliability)

    for rf in reliabilityFrontiers:
        latArray.append(rf['lat'])
        lonArray.append(rf['lon'])

        #Calculate the LCOE
        storVals = np.array(rf['rf'][rKey]['stor'])*dailyLoad
        storCost = storVals*storageCost
        solVals = np.array(rf['rf'][rKey]['sol'])*dailyLoad
        solCost = solVals*solarCost
        minInd = np.argmin(storCost+solCost)
        capitalCost = storCost[minInd]+solCost[minInd]+peakCapacity*capacityCost+fixedCost
        LCOEVal = (crf+oAndMFactor)*capitalCost/365/dailyLoad/reliability

        LCOE.append(LCOEVal)
        hoverText.append(('Lat: {}<br>Lon: {}<br>LCOE ({}/kWh): {:0.3f}<br>kW PV: {:0.2f}<br>kWh Stor: {:0.2f}<br>Capital Cost ({}): {}').format(
            rf['lat'],rf['lon'],currency,LCOEVal,solVals[minInd],storVals[minInd],currency,int(round(capitalCost))
        ))

    (_,binEdges) = np.histogram(LCOE,len(colorscale))
    #for edge in binEdges:
    #    cm
    #cm = dict(zip(bins, colorscale))

    data = [dict(
        lat = latArray,
        lon = lonArray,
        text = hoverText,
        type = 'scattermapbox',
        hoverinfo = 'text',
        marker = dict(size=5, color='white', opacity=0)
    )]

    annotations = [dict(
		showarrow = False,
		#align = 'right',
		text = '<b>LCOE</b>',
		x = 0.95,
		y = 0.95,
	)]

    for i in range(0,len(colorscale)):
        #color = cm[bin]
        annotations.append(
            dict(
                arrowcolor = colorscale[i],
                text = ('{:0.3f}-{:0.3f}').format(binEdges[i],binEdges[i+1]),
                x = 0.95,
                y = 0.85-(i/20),
                ax = -55,
                ay = 0,
                arrowwidth = 8,
                arrowhead = 0,
                bgcolor = '#EFEFEE'
            )
        )

    if 'layout' in figure:
        lat = figure['layout']['mapbox']['center']['lat']
        lon = figure['layout']['mapbox']['center']['lon']
        zoom = figure['layout']['mapbox']['zoom']
    else:
        lat = 0
        lon = 20
        zoom = 2

    layout = dict(
        mapbox = dict(
            layers = [],
            accesstoken = mapboxToken,
            style = 'light',
            center=dict(lat=lat, lon=lon),
            zoom=zoom
        ),
        hovermode = 'closest',
        margin = dict(r=0, l=0, t=0, b=0),
        annotations = annotations,
        dragmode = 'lasso'
    )

    binInd = np.digitize(LCOE,binEdges[:-1])#temporary hack
    geoJSONBinned = [{
        'type': 'FeatureCollection',
        'features': []
        } for i in range(len(colorscale))]

    for i in range(len(LCOE)):
        layerInd = binInd[i]-1
        lon = lonArray[i]
        lat = latArray[i]
        geoJSONBinned[layerInd]['features'].append({
            'type': 'Feature',
            'properties':{},
            'geometry': {
                'type': 'Polygon',
                'coordinates': [
                    [
                        [lon, lat],
                        [lon+resolution, lat],
                        [lon+resolution, lat+resolution],
                        [lon, lat+resolution],
                        [lon, lat]
                    ]
                ]
            }
        })

    #Dump geojson for debugging
    # for i in range(len(geoJSONBinned)):
    #     with open(('debug/geojsonOut_{}.json').format(i),'w') as outfile:
    #         json.dump(geoJSONBinned[i],outfile)

    for i in range(len(colorscale)):
        geoLayer = dict(
            sourcetype = 'geojson',
            source = geoJSONBinned[i],
            type = 'fill',
            color = colorscale[i],
            opacity = 0.8
        )
        layout['mapbox']['layers'].append(geoLayer)

    fig = dict(data=data, layout=layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
