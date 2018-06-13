import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

import numpy as np
import json

from utilities import getReliabilityValue
from globals import MAPBOX_TOKEN,DEFAULT_COLORSCALE
from layout import layout

colorscale = DEFAULT_COLORSCALE
#mapboxToken = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2oyY2M4YW55MDF1YjMzbzhmemIzb290NiJ9.sT6pncHLXLgytVEj21q43A'

reliabilityFrontiers = json.load(open('reliabilityFrontiers_constant_africa_1.json'))

app = dash.Dash(__name__)
app.title = 'Cost of Reliability'
server = app.server
app.css.append_css({
    #'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'
})

app.layout = layout

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
        Input('buttonUpdateMap2','n_clicks')
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
    fixedCost,oAndMFactor,term,discountRate,currency,oldFigure):

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
        bgcolor = '#EFEFEE',
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

    if 'layout' in oldFigure:
        lat = oldFigure['layout']['mapbox']['center']['lat']
        lon = oldFigure['layout']['mapbox']['center']['lon']
        zoom = oldFigure['layout']['mapbox']['zoom']
    else:
        lat = 0
        lon = 20
        zoom = 2

    layout = dict(
        mapbox = dict(
            layers = [],
            accesstoken = MAPBOX_TOKEN,
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

    newFigure = dict(data=data, layout=layout)
    return newFigure

if __name__ == '__main__':
    app.run_server(debug=True)
