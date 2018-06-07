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
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/dZVMbK.css"})

DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", \
	"#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", \
	"#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]

colorscale = DEFAULT_COLORSCALE

mapboxToken = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2oyY2M4YW55MDF1YjMzbzhmemIzb290NiJ9.sT6pncHLXLgytVEj21q43A'

reliabilityFrontiers = json.load(open('reliabilityFrontiers_constant_africa_1.json'))

#Technical parameters
sampleReliabilities = 1-np.divide(0.1,np.power(2.,np.arange(-2,11)))
DEFAULT_DAILY_LOAD = 8.2 # kWh/day
DEFAULT_PEAK_CAPACITY = 2 #kW
DEFAULT_SOLAR_DERATE = 85 #percent
DEFAULT_BATTERY_LIFETIME = 10 #years

#Economic parameters
DEFAULT_BATTERY_COST = 400 #$/kWh
DEFAULT_SOLAR_COST = 1000 #$/kW
DEFAULT_CHARGE_CONTROLLER_COST = 200 #$/kW
DEFAULT_CAPACITY_COST = 1300 #$/kW of peak load rest
DEFAULT_FIXED_COST = 0 #$
DEFAULT_OM_FACTOR = 5 #(%)
DEFAULT_TERM = 20 #years
DEFAULT_DISCOUNT_RATE= 10 #per year

app.layout = html.Div([
    html.H1('[Under Construction]'),
    html.H1('Estimated Cost of Decentralized Solar Power Systems in sub-Saharan Africa'),
    html.Hr(),
    html.Div(
        children=[
            html.H2('Parameters'),
            html.Button(id='buttonUpdateMap', n_clicks=0, children='Update Map'),
            html.Hr(),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H3('Technical'),
                            html.Label('Target reliability (Fraction of Demand Served)'),
                            html.Div(children=[dcc.Slider(
                                id='sliderReliability',
                                min=np.amin(sampleReliabilities),
                                max=np.amax(sampleReliabilities),
                                value=sampleReliabilities[round(len(sampleReliabilities)/2)],
                                step=None,
                                marks={str(r): str(r) for r in sampleReliabilities},
                            )],style={'padding-bottom':20}),
                            html.Label('Daily Load (kWh/day)'),
                            dcc.Input(
                                id='inputDailyLoad',type='number',value=DEFAULT_DAILY_LOAD
                            ),
                            html.Label('Peak Capacity (kW)'),
                            dcc.Input(
                                id='inputPeakCapacity',type='number',value=DEFAULT_PEAK_CAPACITY
                            ),
                            html.Label('Solar Derating (%)'),
                            dcc.Input(
                                id='inputSolarDerate',type='number',value=DEFAULT_SOLAR_DERATE,
                                    min=0,max=100
                            ),
                            html.Label('Battery Lifetime (yrs)'),
                            dcc.Input(
                                id='inputBatteryLifetime',type='number',value=DEFAULT_BATTERY_LIFETIME
                            )
                        ],
                        className="six columns"
                    ),
                    html.Div(
                        children=[
                            html.H3('Economic'),
                            html.Label('Battery Cost (USD/kWh)'),
                            dcc.Input(
                                id='inputBatteryCost',type='number',value=DEFAULT_BATTERY_COST
                            ),
                            html.Label('Solar Cost (USD/kW, including racking'),
                            dcc.Input(
                                id='inputSolarCost',type='number',value=DEFAULT_SOLAR_COST
                            ),
                            html.Label('Charge Controller Cost (USD/kW)'),
                            dcc.Input(
                                id='inputChargeControllerCost',type='number',
                                value=DEFAULT_CHARGE_CONTROLLER_COST
                            ),
                            html.Label('Capacity Cost (USD/kW) - Includes inverter/DC power supply, balance-of-system, etc.; i.e. variable costs per peak capacity'),
                            dcc.Input(
                                id='inputCapacityCost',type='number',value=DEFAULT_CAPACITY_COST
                            ),
                            html.Label('Additional Fixed Cost (USD)'),
                            dcc.Input(
                                id='inputFixedCost',type='number',value=DEFAULT_FIXED_COST
                            ),
                            html.Label('Operations and Maintenance Factor (% of total capital cost)'),
                            dcc.Input(
                                id='inputOMFactor',type='number',value=DEFAULT_OM_FACTOR
                            ),
                            html.Label('Project Term (yrs)'),
                            dcc.Input(
                                id='inputTerm',type='number',value=DEFAULT_TERM
                            ),
                            html.Label('Discount Rate (%)'),
                            dcc.Input(
                                id='inputDiscountRate',type='number',value=DEFAULT_DISCOUNT_RATE,
                                    min=0,max=100
                            )
                        ],
                        className="six columns"
                    )
                ]
            )
        ],
        className='four columns'
    ),
    html.Div(
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
                            'zoom': 2.5,
                            'pitch': 0
                        }
                    }
                })
        ],
        className='six columns'
    )
])


@app.callback(
    dash.dependencies.Output('map','figure'),
    [Input('buttonUpdateMap','n_clicks')],
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
        State('map', 'figure')
    ]
)
def display_map(n_clicks,reliability,dailyLoad,peakCapacity,solarDerate,
    batteryLifetime,storageCost,solarCost,chargeControllerCost,capacityCost,
    fixedCost,oAndMFactor,term,discountRate,figure):

    #Convert percentage to per unit
    discountRate = discountRate/100
    solarDerate = solarDerate/100
    oAndMFactor = oAndMFactor/100

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
        hoverText.append(('Lat: {}<br>Lon: {}<br>LCOE: {:0.3f}<br>kW PV: {:0.2f}<br>kWh Stor: {:0.2f}<br>Capital Cost: {}').format(
            rf['lat'],rf['lon'],LCOEVal,solVals[minInd],storVals[minInd],round(capitalCost)
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
                ax = -60,
                ay = 0,
                arrowidth = 5,
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
        zoom = 2.5

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
