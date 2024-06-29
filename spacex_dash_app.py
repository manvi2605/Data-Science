# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),

    # TASK 1: Dropdown list for Launch Site selection
    html.Div([
        dcc.Dropdown(id='site-dropdown',
                     options=[{'label': 'All Sites', 'value': 'ALL'}] +
                             [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                     value='ALL',
                     placeholder="Select a Launch Site here",
                     searchable=True),
    ],
        style={'width': '80%', 'margin': 'auto'}
    ),

    html.Br(),

    # TASK 2: Pie chart for showing total successful launches count
    html.Div([
        dcc.Graph(id='success-pie-chart'),
    ],
        style={'width': '80%', 'margin': 'auto'}
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Slider for selecting payload range
    html.Div([
        dcc.RangeSlider(id='payload-slider',
                        min=min_payload, max=max_payload, step=1000,
                        marks={i: str(i) for i in range(min_payload, max_payload + 1, 1000)},
                        value=[min_payload, max_payload]),
    ],
        style={'width': '80%', 'margin': 'auto'}
    ),

    html.Br(),

    # TASK 4: Scatter chart for showing correlation between payload and launch success
    html.Div([
        dcc.Graph(id='success-payload-scatter-chart'),
    ],
        style={'width': '80%', 'margin': 'auto'}
    ),
])


# TASK 2: Callback function for updating success pie chart based on selected launch site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
        title = "Success Rate for All Sites"
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f"Success Rate for {selected_site}"

    success_counts = filtered_df['class'].value_counts()
    fig = px.pie(names=success_counts.index,
                 values=success_counts.values,
                 title=title,
                 labels={'0': 'Failure', '1': 'Success'})
    return fig


# TASK 4: Callback function for updating scatter chart based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df
        title = "Payload vs. Success Rate for All Sites"
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f"Payload vs. Success Rate for {selected_site}"

    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (filtered_df['Payload Mass (kg)'] <= payload_range[1])]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title=title,
                     labels={'class': 'Outcome'})
    fig.update_layout(yaxis=dict(tickvals=[0, 1], ticktext=['Failure', 'Success']))
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
