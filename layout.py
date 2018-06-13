import dash_html_components as html
import dash_core_components as dcc

from globals import SAMPLE_RELIABILITY_EXPONENTS,DEFAULT_PEAK_CAPACITY,DEFAULT_DAILY_LOAD,DEFAULT_SOLAR_DERATE,DEFAULT_BATTERY_LIFETIME,DEFAULT_CURRENCY,DEFAULT_BATTERY_COST,DEFAULT_SOLAR_COST,DEFAULT_CHARGE_CONTROLLER_COST,DEFAULT_CAPACITY_COST,DEFAULT_FIXED_COST,DEFAULT_OM_FACTOR,DEFAULT_TERM,DEFAULT_DISCOUNT_RATE,MAPBOX_TOKEN
from utilities import getReliabilityValue
from descriptionText import topText


parameterSectionTechnicalItems=[
    html.H3('Technical'),
    html.Hr(),
    html.Div(
        #className='row col-sm-12',
        children=[
            html.Label('Target reliability (Fraction of Demand Served)'),
            html.Div(children=[dcc.Slider(
                id='sliderReliability',
                min=SAMPLE_RELIABILITY_EXPONENTS[0],
                max=SAMPLE_RELIABILITY_EXPONENTS[-1],
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

layout = html.Div(
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
                dcc.Markdown(topText),
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
                                'data': []#,
                                # 'layout': {
                                #     'mapbox': {
                                #         'layers': [],
                                #         'accesstoken': MAPBOX_TOKEN,
                                #         'center': {
                                #             'lat': 0,
                                #             'lon': 20,
                                #         },
                                #         'zoom': 2,
                                #         'pitch': 0
                                #     }
                                # }
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
