import ast
import configparser
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import json
import numpy as np
import pandas as pd
import urllib

from utilities import calculateMinimumCost, getLoadProfile, getReliabilityValue
from globals import MAPBOX_TOKEN,DEFAULT_COLORSCALE,SAMPLE_RELIABILITY_EXPONENTS
from layout import layout


try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    DEBUG = ast.literal_eval(config['DEFAULT']['DEBUG'])
    PORT = config['DEFAULT']['PORT']
    URL_BASE_PATHNAME = config['DEFAULT']['URL_BASE_PATHNAME']
    ROUTES_PATHNAME_PREFIX = config['DEFAULT']['ROUTES_PATHNAME_PREFIX']
    REQUESTS_PATHNAME_PREFIX = config['DEFAULT']['REQUESTS_PATHNAME_PREFIX']
except (IOError, KeyError):
    DEBUG = False
    PORT = 8050
    URL_BASE_PATHNAME = '/'
    ROUTES_PATHNAME_PREFIX = '/'
    REQUESTS_PATHNAME_PREFIX = '/'

colorscale = DEFAULT_COLORSCALE

reliabilityFrontiersLoadType = {}
loadProfileNames = [
    'constant', 'representative', 'dayHeavy', 'nightHeavy', 'smallIndia'#,
    # 'mediumHouseholds', 'saGrid', 'loadZim', 'homeBusiness', 'onlyBusinesses'
]
resolution = 1
for lpn in loadProfileNames:
    reliabilityFrontiersLoadType[lpn] = json.load(open('reliabilityFrontiers/reliabilityFrontiers_{}_africa_{}.json'.format(lpn,resolution)))

app = dash.Dash(name=__name__,url_base_pathname=URL_BASE_PATHNAME)
app.config.update({
    'routes_pathname_prefix': ROUTES_PATHNAME_PREFIX,
    'requests_pathname_prefix': REQUESTS_PATHNAME_PREFIX
})

app.title = 'Cost of Reliability'
server = app.server
app.css.append_css({
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

@app.callback(Output('graphLoadProfiles','figure'),
    [
        Input('inputDailyLoad','value'),
        Input('inputLoadProfileName','value')
])
def display_load(dailyLoad,loadProfileName):
    loadProfileValues = list(getLoadProfile(loadProfileName)*dailyLoad)
    return {
        'data': [{
            'x': list(range(24)),
            'y': loadProfileValues,
            'mode':'lines',
            'line': {'width':3}
        }],
        'layout': {
            'xaxis': {
                'range': [0,24],
                'tickvals': [0,4,8,12,16,20,24],
                'title': 'Hour of day'
            },
            'yaxis': {
                'range': [0,max(loadProfileValues)*1.5],
                'title': 'kW'
            },
            'title': 'Selected Load Profile'
        }
    }

@app.callback(
    Output('map','figure'),
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
        State('inputLoadProfileName','value'),
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
    batteryLifetime,loadProfileName,storageCost,solarCost,chargeControllerCost,capacityCost,
    fixedCost,oAndMFactor,term,discountRate,currency,oldFigure):

    reliabilityFrontiers = reliabilityFrontiersLoadType[loadProfileName]

    latArray = []
    lonArray = []
    LCOE = []
    initialCostArray = []
    replacementCostArray = []
    capitalCostArray = []
    oAndMCostArray = []
    solCapArray = []
    storCapArray = []
    hoverText = []

    for rf in reliabilityFrontiers:
        latArray.append(rf['lat'])
        lonArray.append(rf['lon'])

        minCost = calculateMinimumCost(
            reliabilityFrontier = rf,
            reliability = getReliabilityValue(reliabilityExponent),
            dailyLoad = dailyLoad,
            peakCapacity = peakCapacity,
            solarDerate = solarDerate/100,
            storageCost = storageCost,
            solarCost = solarCost,
            chargeControllerCost = chargeControllerCost,
            capacityCost = capacityCost,
            fixedCost = fixedCost,
            oAndMFactor = oAndMFactor/100,
            discountRate = discountRate/100,
            term = term,
            batteryLifetime = batteryLifetime
        )

        LCOE.append(minCost['LCOE'])
        initialCostArray.append(minCost['initialCost'])
        replacementCostArray.append(minCost['replacementCost'])
        capitalCostArray.append(minCost['capitalCost'])
        oAndMCostArray.append(minCost['oAndMCost'])
        solCapArray.append(minCost['solarCapacity'])
        storCapArray.append(minCost['storageCapacity'])

        hoverText.append(('Lat: {}<br>Lon: {}<br>LCOE ({}/kWh): {:0.3f}<br>kW PV: {:0.2f}<br>kWh Stor: {:0.2f}<br>Capital Cost ({}): {}').format(
            rf['lat'],rf['lon'],currency,minCost['LCOE'],minCost['solarCapacity'],minCost['storageCapacity'],currency,int(round(minCost['capitalCost']))
        ))

    (_,binEdges) = np.histogram(LCOE,len(colorscale))
    #for edge in binEdges:
    #    cm
    #cm = dict(zip(bins, colorscale))

    data = [dict(
        lat = [x + resolution/2 for x in latArray], #offset to put data in middle of square
        lon = [x + resolution/2 for x in lonArray],
        LCOE = LCOE,
        solCap = solCapArray,
        storCap = storCapArray,
        capCost = capitalCostArray,
        initCost = initialCostArray,
        repCost = replacementCostArray,
        oAndMCost = oAndMCostArray,
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
		x = 0.90,
		y = 0.915,
	)]

    for i in range(0,len(colorscale)):
        #color = cm[bin]
        annotations.append(
            dict(
                arrowcolor = colorscale[i],
                text = ('{:0.3f}-{:0.3f}').format(binEdges[i],binEdges[i+1]),
                height = 21,
                x = 0.95,
                y = 0.85-(i/20),
                ax = -55,
                ay = 0,
                arrowwidth = 23,
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
        dragmode = 'select'
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
            opacity = 0.7
        )
        layout['mapbox']['layers'].append(geoLayer)

    newFigure = dict(data=data, layout=layout)
    return newFigure

@app.callback(Output('downloadLinkMap','href'),
    [Input('map', 'figure')])
def updateLink(figure):
    d = figure['data'][0]
    df = pd.DataFrame({
        'lat': d['lat'],
        'lon': d['lon'],
        'LCOE': d['LCOE'],
        'Up-front Cost': d['initCost'],
        'Replacement Cost (Present Cost)': d['repCost'],
        'Total Capital Cost': d['capCost'],
        'O And M Cost': d['oAndMCost'],
        'Solar Capacity (kW)': d['solCap'],
        'Storage Capacity (kWh)': d['storCap']
    },
    columns=['lat','lon','LCOE','Up-front Cost','Replacement Cost (Present Cost)','Total Capital Cost','O And M Cost','Solar Capacity (kW)','Storage Capacity (kWh)'])
    return 'data:text/csv;charset=utf-8,'+urllib.parse.quote(df.to_csv(index=False, encoding='utf-8'))


@app.callback(
    Output('downloadLinkLCOE', 'href'),
    [Input('selectedDataReliabilityScaling', 'figure')]
)
def updateLinkLCOE(figure):
    d = figure['data'][0]
    df1 = pd.DataFrame(
        np.column_stack((d['lat'], d['lon'])),
        columns=['lat', 'lon']
    )
    df2 = pd.DataFrame(
        data=d['LCOE'],
        columns=[
            'LCOE @ FDS={:0.2f}%'.format(getReliabilityValue(r)*100)
            for r in SAMPLE_RELIABILITY_EXPONENTS
        ]
    )
    df = pd.concat([df1, df2], axis=1)
    return 'data:text/csv;charset=utf-8,'+urllib.parse.quote(
        df.to_csv(index=False, encoding='utf-8')
    )

@app.callback(Output('selectedDataReliabilityScaling','figure'),
    [
        Input('map','selectedData'),
        Input('map','figure')
    ],
    [
        State('inputDailyLoad','value'),
        State('inputPeakCapacity','value'),
        State('inputSolarDerate','value'),
        State('inputBatteryLifetime','value'),
        State('inputLoadProfileName','value'),
        State('inputBatteryCost','value'),
        State('inputSolarCost','value'),
        State('inputChargeControllerCost','value'),
        State('inputCapacityCost','value'),
        State('inputFixedCost','value'),
        State('inputOMFactor','value'),
        State('inputTerm','value'),
        State('inputDiscountRate','value'),
        State('inputCurrency','value')
    ])
def displaySelectedReliabilityScaling(selectedData,figure,dailyLoad,peakCapacity,solarDerate,
    batteryLifetime,loadProfileName,storageCost,solarCost,chargeControllerCost,capacityCost,
    fixedCost,oAndMFactor,term,discountRate,currency):

    reliabilityFrontiers = reliabilityFrontiersLoadType[loadProfileName]

    if selectedData is None:
        showAll = True
        points = np.zeros((len(reliabilityFrontiers),1))
    else:
        showAll = False
        points = [(p['lat']-resolution/2,p['lon']-resolution/2) for p in selectedData['points']]

    LCOE = np.zeros((len(points), len(SAMPLE_RELIABILITY_EXPONENTS)))
    lat = np.zeros((len(points)))
    lon = np.zeros((len(points)))

    rowInd = 0
    for rf in reliabilityFrontiers:
        if not showAll and (rf['lat'],rf['lon']) not in points:
            continue

        for colInd,reliabilityExponent in enumerate(SAMPLE_RELIABILITY_EXPONENTS):
            reliability = getReliabilityValue(reliabilityExponent)

            LCOE[rowInd,colInd] = calculateMinimumCost(
                reliabilityFrontier = rf,
                reliability = reliability,
                dailyLoad = dailyLoad,
                peakCapacity = peakCapacity,
                solarDerate = solarDerate/100,
                storageCost = storageCost,
                solarCost = solarCost,
                chargeControllerCost = chargeControllerCost,
                capacityCost = capacityCost,
                fixedCost = fixedCost,
                oAndMFactor = oAndMFactor/100,
                discountRate = discountRate/100,
                term = term,
                batteryLifetime = batteryLifetime
            )['LCOE']

            lat[rowInd] = rf['lat']
            lon[rowInd] = rf['lon']

        rowInd += 1

    #print(LCOE)
    nBins = 30
    ymin = np.amin(LCOE)
    ymax = np.amax(LCOE)
    ymax2 = ymin
    for i in range(0,len(SAMPLE_RELIABILITY_EXPONENTS)):
        #print(np.histogram(LCOE[:,i],bins = nBins,range=(ymin,ymax),density=True))
        (hist,y) = np.histogram(LCOE[:,i],bins = nBins,range=(ymin,ymax),density=False)
        ymax2 = max(ymax2,y[np.sum(np.cumsum(hist/len(points)) < 0.95)]) #Find the point where 95% of the cumulative distribution is captured, and use that to set the upper bound

    z = np.zeros((nBins,len(SAMPLE_RELIABILITY_EXPONENTS)))
    #Re-calculate the histogram with the appropriate upper bound
    for i in range(0,len(SAMPLE_RELIABILITY_EXPONENTS)):
        #print(np.histogram(LCOE[:,i],bins = nBins,range=(ymin,ymax),density=True))
        (hist,y) = np.histogram(LCOE[:,i],bins = nBins,range=(ymin,ymax2),density=False)
        z[:,i] = hist/len(points)

    return {
        'data': [{
            'z': z,
            'x': list(SAMPLE_RELIABILITY_EXPONENTS),
            'y': y,
            'type': 'heatmap',
            'colorscale': 'Viridis',
            'colorbar': {
                'title': 'Density'
            },
            'LCOE': LCOE,  # Only b/c need to pass this to download link
            'lat': lat,  # Only b/c need to pass this to download link
            'lon': lon  # Only b/c need to pass this to download link
        }],
        'layout': {
            'title': 'Scaling of LCOE vs Reliability for Selected Locations<br>(click and drag on map)',
            'xaxis': {
                'title': 'Fraction of Demand Served (%)',
                'tickvals': list(SAMPLE_RELIABILITY_EXPONENTS),
                'ticktext': ['{:0.2f}'.format(getReliabilityValue(r)*100) for r in SAMPLE_RELIABILITY_EXPONENTS]
            },
            'yaxis': {
                'title': 'LCOE ({})'.format(currency)
            }
        }
    }

if __name__ == '__main__':
    app.run_server(debug=DEBUG,port=PORT)
