
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

my_file = input('enter file path')
df = pd.read_csv(my_file)

all_options = df['category'].unique()

app.layout = html.Div([

    dcc.Dropdown(
        id='category_type',
        options=[
        {'label': k , 'value': k} for k in all_options
        ],
        value=['Expense: Housing'],
        multi=True
        ),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
            go.Scatter(
                x=df[df['category']==i]['date'],
                y=df[df['category']==i]['debit'],
                text=df[df['category']==i]['subcategory'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 8,
                    'line': { 'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df['category'].unique()
        ],
        'layout': go.Layout(
            xaxis={'title':'Date'},
            yaxis={'type':'currency','title': 'Amount'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x':0, 'y':-1},
            hovermode='closest'
            )
        }
    )
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('category_type','value')])

def update_graph(category_type):
    filtered_df = df[df['category'].isin(set(category_type))]
    print(category_type)
    traces = []

    for i in filtered_df['category'].unique():
        df_by_category = filtered_df[filtered_df['category'] == i ]
        traces.append(go.Scatter(
            x=df_by_category['date'],
            y=df_by_category['debit'],
            text=df_by_category['subcategory'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 8,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title':'Date'},
            yaxis={'type':'currency','title': 'Amount'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x':0, 'y':-1},
            hovermode='closest'
            )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
