# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Get unique launch sites for the dropdown options
launch_sites = spacex_df['Launch Site'].unique().tolist()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_sites:
    dropdown_options.append({'label': site, 'value': site})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                         style={'textAlign': 'center', 'color': '#503D36',
                                                'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=dropdown_options,
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0 kg',
                                                       2500: '2500 kg',
                                                       5000: '5000 kg',
                                                       7500: '7500 kg',
                                                       10000: '10000 kg'},
                                                value=[min_payload, max_payload]
                                ),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# ----------------------------------------------------------------------
# TASK 2: Callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Calculate total success for all sites
        total_success = spacex_df[spacex_df['class'] == 1].groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(total_success, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Successful Launches By Site')
        return fig
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count success (class=1) and failure (class=0)
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']
        # Map 1 to Success and 0 to Failure for better labeling
        success_counts['class'] = success_counts['class'].map({1: 'Success', 0: 'Failure'})
        
        fig = px.pie(success_counts, 
                     values='count', 
                     names='class', 
                     title=f'Total Success vs. Failure Launches for site {entered_site}')
        return fig

# ----------------------------------------------------------------------
# TASK 4: Callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    # Filter by payload range first
    low, high = payload_range
    filtered_payload_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) & 
        (spacex_df['Payload Mass (kg)'] <= high)
    ]
    
    if entered_site == 'ALL':
        # Plot all sites within the payload range
        fig = px.scatter(filtered_payload_df, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        # Filter by site and payload range
        filtered_site_df = filtered_payload_df[filtered_payload_df['Launch Site'] == entered_site]
        
        fig = px.scatter(filtered_site_df, 
                         x='Payload Mass (kg)', 
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig


# Run the app
if __name__ == '__main__':
    app.run()