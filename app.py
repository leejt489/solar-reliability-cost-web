import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_colorscales
from dash.dependencies import Input, Output, State

import numpy as np
import json


app = dash.Dash()
app.scripts.config.serve_locally=True
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/dZVMbK.css"})

DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", \
	"#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", \
	"#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]

colorscale = DEFAULT_COLORSCALE

mapboxToken = 'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2oyY2M4YW55MDF1YjMzbzhmemIzb290NiJ9.sT6pncHLXLgytVEj21q43A'

reliabilityFrontiers = json.load(open('reliabilityFrontiers_constant_africa_1.json'))

sampleReliabilities = 1-np.divide(0.1,np.power(2.,np.arange(-2,11)))

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    html.H1('Estimated Cost of Decentralized Solar Power Systems in sub-Saharan Africa'),
    html.Hr(),
    html.Div(
        children=[
            html.P('Target reliability (Fraction of Demand Served)'),
            dcc.Slider(
                id='sliderReliability',
                min=np.amin(sampleReliabilities),
                max=np.amax(sampleReliabilities),
                value=sampleReliabilities[round(len(sampleReliabilities)/2)],
                step=None,
                marks={str(r): str(r) for r in sampleReliabilities}
            ),
            html.P('Map of levelized cost of electricity (LCOE)'),
            dcc.Graph(
                id='map',
                #animate=True,
                figure = {
                    'data': [],
                    'layout': {
                        'mapbox': {
                            'layers': [],
                            'accesstoken': mapboxToken,
                            'style': 'light',
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
    [dash.dependencies.Input('sliderReliability','value')],
    [State('map', 'figure')]
)
def display_map(reliability,figure):

    #print(reliability)

    storageCost = 400 #$/kWh
    solarCost = 1000 #$/kW
    dailyLoad = 8.2 # kWh/day
    peakLoad = 2 #kW
    boSCost = (300+1000)*peakLoad #soft and hardware costs, $300 per kW inverter + $1000 rest
    oAndMFactor = 0.05 #per unit of total capital cost per year
    term = 20 #years
    discountRate = 0.1 #per year
    batteryLifetime = 10 #years
    solarDerate = 0.85
    chargeControllerCost = 200; # $/kW (gets added to solarCost)

    solarCost = solarCost/solarDerate+chargeControllerCost #Solar lifetime assumed to be term
    storageCost = storageCost*(1-(1-discountRate)**term)/(1-(1-discountRate)**batteryLifetime) #Includes replacement cost of storage
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
        storCost = np.array(rf['rf'][rKey]['stor'])*storageCost
        solCost = np.array(rf['rf'][rKey]['sol'])*solarCost
        minSolStorCost = np.amin(storCost+solCost)
        capitalCost = minSolStorCost+boSCost
        LCOEVal = (crf+oAndMFactor)*capitalCost/365/dailyLoad/reliability

        LCOE.append(LCOEVal)
        hoverText.append(('LCOE: {:0.3f}').format(LCOEVal))

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

    for i in range(len(geoJSONBinned)):
        with open(('debug/geojsonOut_{}.json').format(i),'w') as outfile:
            json.dump(geoJSONBinned[i],outfile)

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

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/dZVMbK.css"
})

if __name__ == '__main__':
    app.run_server(debug=True)
