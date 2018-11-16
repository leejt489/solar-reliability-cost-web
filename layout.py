import dash_html_components as html
import dash_core_components as dcc

from globals import SAMPLE_RELIABILITY_EXPONENTS,DEFAULT_PEAK_CAPACITY,DEFAULT_DAILY_LOAD,DEFAULT_SOLAR_DERATE,DEFAULT_BATTERY_LIFETIME,DEFAULT_CURRENCY,DEFAULT_BATTERY_COST,DEFAULT_SOLAR_COST,DEFAULT_CHARGE_CONTROLLER_COST,DEFAULT_CAPACITY_COST,DEFAULT_FIXED_COST,DEFAULT_OM_FACTOR,DEFAULT_TERM,DEFAULT_DISCOUNT_RATE,MAPBOX_TOKEN
from utilities import getReliabilityValue
from descriptionText import topText, guideText, researchersText


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
                marks={str(r): '{:0.2f}'.format(getReliabilityValue(r)*100) for r in SAMPLE_RELIABILITY_EXPONENTS[::2]}
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
    ),
    html.Div(
        className='row',
        children=[
            html.Div(html.Label('Daily load profile'),className='col-lg-6'),
            html.Div(dcc.Dropdown(
                id='inputLoadProfileName',
                options=[
                    {'label': 'Constant', 'value': 'constant'},
                    {'label': 'Uganda Mini-grid', 'value': 'representative'},
                    {'label': 'Day Heavy', 'value': 'dayHeavy'},
                    {'label': 'Night Heavy', 'value': 'nightHeavy'},
                    {'label': 'Small India', 'value': 'smallIndia'},
                    {'label': 'Medium Households', 'value': 'mediumHouseholds'},
                    {'label': 'South African Grid Connected', 'value': 'saGrid'},
                    {'label': 'Zimbabwe', 'value': 'loadZim'},
                    {'label': 'Homes Plus Businesses', 'value': 'homeBusiness'},
                    {'label': 'Only Businesses', 'value': 'onlyBusinesses'}
                ],
                value='constant'
            ),className='col-lg-6')
        ]
    ),
    html.Div(
        className='row',
        children=[
            dcc.Graph(
                id='graphLoadProfiles',
                figure={
                    'data': [],
                    'layout': {}
                },
                config={'displayModeBar': False}
            )
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
    html.Button(id='buttonUpdateMap', n_clicks=0, children='Update Graph', className="btn btn-primary"),
    html.Hr(),
    html.Div(
        className='row',
        children=[
            html.Div(
                children=parameterSectionTechnicalItems,
                className="col-lg-6"
            ),
            html.Div(
                children=parameterSectionEconomicItems,
                className="col-lg-6"
            )
        ]
    ),
    html.Hr(),
    html.Button(id='buttonUpdateMap2', children='Update Map', className="btn btn-primary")
]

layout = html.Div(
    className='container-fluid',
    children=[
        html.Div(
            className='row col-xs-12',
            children=[
                html.H1('Estimated Cost of Electricity and Reliability for Decentralized Solar Power Systems in sub-Saharan Africa'),
                html.H3('[Beta Version]'),
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
                    className='col-lg-7 col-md-5',
                    children=parameterSectionItems
                ),
                html.Div(
                    className='col-lg-5 col-md-7',
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
                            },
                            config = {
                                #'modeBarButtonsToAdd': ['zoom2d'],
                                'modeBarButtonsToRemove': ['toggleHover','sendDataToCloud']
                            }
                        ),
                        html.A(
                            html.Button('Download Map Data as CSV',className='btn btn-primary'),
                            id='downloadLinkMap',
                            download="rawdata.csv",
                            href="",
                            target="_blank"
                        ),
                        dcc.Graph(id='selectedDataReliabilityScaling'),
                        html.A(
                            html.Button(
                                'Download LCOE vs. Reliability as CSV',
                                className='btn btn-primary',
                            ),
                            id="downloadLinkLCOE",
                            download="LCOEByReliability.csv",
                            href="",
                            target="_blank"
                        )
                    ]
                )
            ]
        ),
        html.Hr(),
        html.Div(
            id='quickGuide',
            className='row col-xs-12',
            children=[
                dcc.Markdown(guideText),
                html.H3('Load Profiles'),
                html.Div('We have provided a collection of sample average daily load profiles that result in different model outputs. Some are empirically measured and others are estimated or constructed, as described below:'),
                html.Table(
                    [
                        html.Thead(html.Tr([
                            html.Th('Daily Load Profile'),
                            html.Th('Source'),
                            html.Th('Description')
                        ])),
                        html.Tbody([html.Tr([
                            html.Td('Constant'),
                            html.Td('N/A'),
                            html.Td('Constant demand. Unrealistic but simple, and evenly distributes load between nighttime and daytime hours')
                        ]),
                        html.Tr([
                            html.Td('Uganda Mini-grid'),
                            html.Td(html.A('New Sun Road, P.B.C', href='https://www.newsunroad.com', target='_blank')),
                            html.Td('Empirical demand from a village of 34 small business on an island in Lake Victoria, Uganda')
                        ]),
                        html.Tr([
                            html.Td('Day Heavy'),
                            html.Td('N/A'),
                            html.Td('All demand during the hours of 06:00 and 18:00 to represent an extreme case of demand only during the day, which requires very little storage')
                        ]),
                        html.Tr([
                            html.Td('Night Heavy'),
                            html.Td('N/A'),
                            html.Td('All demand during the hours of 18:00 and 06:00 to represent an extreme case of demand only during the night, which requires a large amount of energy storage.. Comparing this with Day Heavy gives some idea of the costs associated with storage and value of shifting load to the day')
                        ]),
                        html.Tr([
                            html.Td('Small India'),
                            html.Td('[...]'),
                            html.Td('[...]')
                        ])])
                    ],
                    className='table table-striped table-bordered'
                ),
                html.Hr()
            ]
        ),
        html.Div(
            id='people',
            className='row col-xs-12',
            children=dcc.Markdown(researchersText)
        ),
        html.Hr(),
        html.Div(
            className='row col-xs-12',
            children=dcc.Markdown('&#169; Jonathan Lee, 2018')
        )
    ]
)
