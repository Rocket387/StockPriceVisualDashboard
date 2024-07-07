#plotly creates the visuals (bar graphs, charts etc)
#dash takes the visuals and incorporates them into a web app for user interaction/ data udpates

#libraries
from yahoofinancials import YahooFinancials
import yfinance as yf
import dash
from dash import Dash, Input, Output, ctx, html, dcc, callback
import pandas_datareader as web
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

# embed custom stylesheets in your dash apps via a custom URL
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css']  # extract the stylesheet from the Codepen playground by appending ".css" to the end of any codepen URL

#Dash app initialization - new instance of the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Stock Visualisation"

#app layout setup
app.layout = html.Div([
    html.H1("Stock Visualisation Dashboard"),
    html.Div(["Input: ",
              dcc.Input(id='input', value='Enter your stock', type='text')]),
    html.Br(),
    html.Button("Submit", id="submit-button", n_clicks=0),
    html.Br(),
    html.H4("Please enter the stock name"),
    html.Div([#Div container
        html.Br(),
        html.Label("Select Time Range:"),
        dcc.Dropdown(
            id='time-range-dropdown',
            options=[
                {'label': '1 Month', 'value': '1M'},
                {'label': '6 Months', 'value': '6M'},
                {'label': '1 Year', 'value': '1Y'},

            ],
            value='1Y', #default value
            clearable=False
        )]),
    #html.Div(id='my-output'),
    dcc.Graph(id='output-graph',
              config={'displayModeBar': 'hover'}),

])

#callback function executes after another function has finished excuting
#this function is called by Dash whenever an input components property changes
#The callback function uses this changed input and returns a new value for an output component’s property.
#Whenever the value of the component with id submit button changes, execute the function underneath
#this decorator and use its return value to update the figure property of the component with id output-graph
@app.callback(
    Output(component_id='output-graph', component_property='figure'),
    [Input(component_id='submit-button', component_property='n_clicks')],
    [Input(component_id='time-range-dropdown', component_property='value')],
    #https://dash.plotly.com/duplicate-callback-outputs for combining inputs (allows for more than one input) into one callback
    [dash.dependencies.State(component_id="input", component_property="value")],
    prevent_initial_call=True #prevents callback being triggered at startup
)
def update_output_div(selected_time_range, n_clicks, value):

    end_date = datetime.today()
    if selected_time_range == '1M':
      start_date = end_date - timedelta(days=30)
    elif selected_time_range == '6M':
      start_date = end_date - timedelta(days=182)
    else:
      start_date = end_date - timedelta(days=365)

    df = yf.download('input', start=start_date, end=end_date)

    tech_stocks = value
    yahoo_financials_tech = YahooFinancials(tech_stocks)
    getName = yahoo_financials_tech.get_stock_quote_type_data()
    df = yahoo_financials_tech.get_historical_price_data("2020-01-01", "2021-03-19", "daily")
    df = pd.DataFrame.from_dict(df[tech_stocks]["prices"])
    fig = px.line(df, x=df['formatted_date'], y=df['close'], labels=dict(x="Date", y="US:OCGN $"), title=getName[tech_stocks]['longName'])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)