
# This dashboard operationalises the exploratory data analysis into an interactive decision-support tool.
# 
# This stage shifts from exploratory analysis to strategic evaluation. Thus, provide visual decision-support through an integrated dashboard
# 
# The analysis focuses on:
# 1. Profitability drivers
# 2. Product inefficiencies
# 3. Pricing strategy effectiveness
# 4. Geographic disparities

# %%
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd 
import plotly.express as px

from urllib.request import urlopen
import json



df= pd.read_csv("superstore_cleaned.csv")




app = Dash(__name__)

app.layout = html.Div([
    html.H2("Superstore Executive Performance Dashboard", 
            style={'textAlign': 'center', 'padding': '20px', 'color': "#6997c5"}),
    
    # KPI Row
    html.Div([
        html.Div([
            html.H4("Total Sales", style={'color': "#2a9d8f"}),
            html.P(f"${df['Sales'].sum():,.2f}", style={'fontSize': '24px', 'fontWeight': 'bold'})
        ], style={'width': '30%', 'display': 'inline-block', 'backgroundColor': "#e2e9f0",
                    'borderRadius': '10px', 'padding': '20px', 'margin': '10px'}),
        html.Div([
            html.H4("Total Profit", style={'color': "#2a9d8f"}),
            html.P(f"${df['Profit'].sum():,.2f}", style={'fontSize': '24px', 'fontWeight': 'bold'})
        ], style={'width': '30%', 'display': 'inline-block', 'backgroundColor': "#e2e9f0",  
                    'borderRadius': '10px', 'padding': '20px', 'margin': '10px'}),
        html.Div([
            html.H4("Average Margin", style={'color': "#2a9d8f"}),
            html.P(f"{(df['Profit'].sum() / df['Sales'].sum()):.2%}", style={'fontSize': '24px', 'fontWeight': 'bold'})
        ], style={'width': '30%', 'display': 'inline-block', 'backgroundColor': "#e2e9f0", 
                    'borderRadius': '10px', 'padding': '20px', 'margin': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'center'}),
    
    # Filter Row
    html.Div([
        html.Div([
            html.Label("Filter by Region:"),
            dcc.Dropdown(id='region-filter', 
                         options=[{'label': i, 'value': i} for i in df['Region'].unique()], 
                         value=df['Region'].unique().tolist(), multi=True)
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Filter by Segment:"),
            dcc.Dropdown(id='segment-filter', 
                         options=[{'label': i, 'value': i} for i in df['Segment'].unique()], 
                         value=df['Segment'].unique().tolist(), multi=True)
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.Label("Filter by Category:"),
            dcc.Dropdown(id='cat-filter', 
                         options=[{'label': i, 'value': i} for i in df['Category'].unique()], 
                         value=df['Category'].unique().tolist(), multi=True)
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'backgroundColor': "#e2e9f0", 'borderRadius': '10px', 'margin': '10px'}),
    
    # Graphics Row
    html.Div([
        dcc.Graph(id='profit-margin-map', style={'width': '100%', 'display': 'inline-block', 'marginTop': '20px'}),
        dcc.Graph(id='profit-margin-sub-category-bar-chart', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='discount-impact-scatter', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='discount-margin-sales', style={'width': '100%', 'display': 'inline-block', 'marginTop': '20px'})
    ])
])

@callback( 
    Output('profit-margin-map', 'figure'),
    Output('profit-margin-sub-category-bar-chart', 'figure'),
    Output('discount-impact-scatter', 'figure'),
    Output('discount-margin-sales', 'figure'),
    Input('region-filter', 'value'),
    Input('segment-filter', 'value'),
    Input('cat-filter', 'value')
)
def update_charts(selected_regions, selected_segments, selected_categories):
    
    # Filter dataset
    filtered_df = df[
        (df['Region'].isin(selected_regions)) & 
        (df['Segment'].isin(selected_segments)) & 
        (df['Category'].isin(selected_categories))
    ]

    # Load GeoJSON
    with urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
        states_geo = json.load(response)

    
    state_summary = filtered_df.groupby('State').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()

    
    state_summary['Profit Margin%'] = (
        state_summary['Profit'] / state_summary['Sales'].replace(0, None)) * 100 # Avoid division by zero 

    # Choropleth map
    map_fig = px.choropleth(
        state_summary,
        geojson=states_geo,
        locations='State',
        featureidkey='properties.name',
        color='Profit Margin%',
        color_continuous_scale='RdBu',
        title='Profit Margin by State'
    )
    map_fig.update_geos(fitbounds="locations", visible=False)

    # Sub-category aggregation
    sub_cat_summary = filtered_df.groupby('Sub-Category').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()

    sub_cat_summary['Profit Margin'] = (
        sub_cat_summary['Profit'] / sub_cat_summary['Sales'].replace(0, None)
    )

    # Bar chart
    bar_chart = px.bar(
        sub_cat_summary,
        x='Sub-Category',
        y='Profit Margin',
        color='Sub-Category',
        title='Profit Margin by Sub-Category',
        text=sub_cat_summary['Profit Margin'].apply(lambda x: f"{x:.2%}")
    )
    bar_chart.update_traces(textposition='outside')

    # Scatter: Discount vs Profit Margin

    scatter = px.scatter(
        filtered_df,
        x="Discount",
        y="Profit Margin",   
        opacity=0.5,
        trendline="ols",
        trendline_color_override="red",
        title="Correlation of Discount and Profit"
    )

    # Scatter: Discount vs Profit (size by Sales)
    discount_sales_scatter = px.scatter(
        filtered_df,
        x="Discount",
        y="Profit",
        size="Sales",
        color="Category",
        hover_name="Sub-Category",
        size_max=60,
        title="Impact of Discounts on Profit (Sized by Sales)"
    )

    return map_fig, bar_chart, scatter, discount_sales_scatter


if __name__ == '__main__':
    app.run(debug=True, port=8051)


# the server will run on http://localhost:8051/
