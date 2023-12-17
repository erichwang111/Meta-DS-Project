import pandas as pd
from dash import Dash,html,Input,Output,dcc
from io import BytesIO
import plotly.express as px
import base64
import dash_bootstrap_components as dbc

def read_html_file(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
    return html_content

def update_index(dash_app):
    df = pd.read_csv("static/data/user_data.csv")
    df2 = pd.read_csv("static/data/user_logins.csv")
    df3 = pd.read_csv("static/data/active_users.csv")
    dash_app.title = "Dashboard"  # Set your dashboard title here
    header_content = read_html_file('templates/header.html')

    dash_app.layout = dbc.Container([
        html.H1("Interactive Data Visualisation",
                style={'textAlign': 'center','color': '#2C2C54','margin-bottom': '30px','margin-top':'30px','font-family':'monospace'}),
        html.P("A Dashboard to monitor/analyze the distribution, recent interests, and activities of the users",
               style={'textAlign':'center','font-family':'monospace','color': '#2C2C54'}),
        dbc.Row([
            dbc.Col([
                html.H2("Consumer distribution",style={'font-family':'monospace','color': '#2C2C54'}),
                html.P("Pie Chart that displays the distribution of the customers by gender/age group.",style={'font-family':'monospace','color': '#2C2C54'}),
                dcc.Dropdown(
                    id="category1",
                    value="age",
                    options=df.columns[1:3],
                )
            ]),
            dbc.Col([
                html.H2("Satisfaction Score",style={'font-family':'monospace','color': '#2C2C54'}),
                html.P("Bar Graph that displays how satisfied the customers are divided by gender/age group.",style={'font-family':'monospace','color': '#2C2C54'}),
                dcc.Dropdown(
                    id = "category2",
                    value = "age",
                    options = df.columns[1:3]
                )
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='graph1',
                          figure={},
                          style={'border':'2px solid #AAABB8','margin-top':'10px','border-radius':'4px','margin-bottom':'20px'})
            ]),
            dbc.Col([
                dcc.Graph(id='graph2',
                          figure={},
                          style={'border':'2px solid #AAABB8','margin-top':'10px','border-radius':'4px'})
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H2("Question Frequency",style={'font-family':'monospace','color': '#2C2C54'}),
                html.P("Bar Graph with a color continuous scale to display how often different types of questions are asked.",style={'font-family':'monospace','color': '#2C2C54'})
            ]),
            dbc.Col([
                html.H2("Daily User Activity",style={'font-family':'monospace','color': '#2C2C54'}),
                html.P("Line Graph that displays the amount of users online by each hour of the day.",style={'font-family':'monospace','color': '#2C2C54'})
            ])
        ]),
        dbc.Row([
            dbc.Col([
            dcc.Graph(id='graph3',
                      figure={},
                      style={'border':'2px solid #AAABB8','margin-top':'10px','border-radius':'4px','margin-bottom':'20px'})
            ]),
            dbc.Col([
            dcc.Graph(id='graph4',
                      figure={},
                      style={'border':'2px solid #AAABB8','margin-top':'10px','border-radius':'4px','margin-bottom':'20px'})
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H2("Monthly User Activity", style={'font-family': 'monospace', 'color': '#2C2C54'}),
                html.P("Line Graph that displays how many customers have logged in every month.",style={'font-family':'monospace','color': '#2C2C54'}),
                dcc.Dropdown(
                    id="category5",
                    value="Total",
                    options=['Total','Gender']
                )
            ])
        ]),
        dbc.Row([
            dcc.Graph(id='graph5',
                      figure={},
                      style={'border': '2px solid #AAABB8', 'margin-top': '10px', 'border-radius': '4px',
                             'margin-bottom': '20px'})
        ])
    ])


    @dash_app.callback(
        Output('graph1', 'figure'),
        Input('category1', 'value')
    )
    def plot_data1(category):
        if category == "gender":
            df_genders = df["gender"].value_counts()
            graph_plotly = px.pie(df,
                                  values=df_genders.values,
                                  names=df_genders.index,
                                  color_discrete_sequence=['#474787','#EAB2BB'],
                                  hover_name=["Male","Female"])
        elif category == "age":
            age_bins = [0,20,30,40,50,]
            age_labels = ["<20","20-29","30-39","40-49"]
            df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels)
            df_age = df.groupby('age_group').size().reset_index(name='User Count')
            df_age = df_age.rename(columns={'age_group':"Age Group"})
            graph_plotly = px.pie(df_age,
                                  values='User Count',
                                  names='Age Group',
                                  color_discrete_sequence=['#2C2C54','#474787','#AAABB8','#ECECEC'],
                                  hover_name=["Under 20","20s","30s","40s"])
        return graph_plotly

    @dash_app.callback(
        Output('graph2', 'figure'),
        Input('category2', 'value')
    )
    def plot_data2(category):
        if category == "gender":
            df_gen = df.groupby("gender")["satisfaction"].mean()
            graph_plotly = px.bar(df_gen,
                                  x=df_gen.index,
                                  y=df_gen,
                                  labels={'x':'Gender','y':'Satisfaction Score'},
                                  color='satisfaction',
                                  color_continuous_scale=[[0.00, "#EAB2BB"], [0.50, "#EAB2BB"],
                                                          [0.50, "#474787"], [1.00, "#474787"]],
                                  hover_name=["Female","Male"])
            graph_plotly.update_layout(plot_bgcolor="#ECECEC")
        elif category == "age":
            age_bins = [0,20,30,40,50,]
            age_labels = ["<20","20-29","30-39","40-49"]
            df["age_group"] = pd.cut(df["age"], bins=age_bins, labels=age_labels)
            df_age = df.groupby('age_group')["satisfaction"].mean()
            df_age = df_age.reindex(["<20","20-29","30-39","40-49"])
            graph_plotly = px.bar(df_age,
                                  x=age_labels,
                                  y=df_age,
                                  labels={'x':'Age Groups','y':'Satisfaction Score'},
                                  hover_name=["Under 20","20s","30s","40s"]
                                  )
            graph_plotly.update_traces(marker_color=['#474787','#2C2C54','#474787','#2C2C54'],
                                       marker_line_color='black',
                                       marker_line_width=1, opacity=1)
            graph_plotly.update_layout(plot_bgcolor="#ECECEC")
        return graph_plotly

    @dash_app.callback(
        Output('graph3', 'figure'),
        Input('category1', 'value')
    )
    def plot_data3(category):
        avg_about = df["about_company"].mean()
        avg_refund = df["refund"].mean()
        avg_topseller = df["topseller"].mean()
        avg_payment = df["payment"].mean()
        avg_discount = df["discount"].mean()
        avg_data = pd.DataFrame({
            'Questions': ["about_company","refund","topseller","payment","discount"],
            "Frequency": [avg_about,avg_refund,avg_topseller,avg_payment,avg_discount]
        })
        graph_plotly = px.bar(avg_data,
                              x='Questions',
                              y='Frequency',
                              color='Frequency',
                              color_continuous_scale=['#AAABB8','#474787'])
        graph_plotly.update_layout(plot_bgcolor="#ECECEC")
        return graph_plotly

    @dash_app.callback(
        Output('graph4', 'figure'),
        Input('category1', 'value')
    )
    def plot_data4(category):
        df2[['Date', 'Time']] = df2["Login Datetime"].str.split(' ',expand=True)
        df2[['Hour', 'Minute', 'Second']] = df2["Time"].str.split(':', expand=True)
        xlabel_hour = ['12AM','1AM','2AM','3AM','4AM','5AM','6AM','7AM','8AM','9AM','10AM','11AM','12PM','1PM','2PM','3PM','4PM','5PM','6PM','7PM','8PM','9PM','10PM','11PM']
        df2_hours = df2.groupby(['Hour']).count()
        df2_data = df2_hours['Date']
        graph_plotly = px.line(df2_hours, x=xlabel_hour, y=df2_data,labels={"x":"Hours","Date":"User Count"})
        graph_plotly.add_scatter(x=xlabel_hour, y=df2_data, line_color="#2C2C54")
        graph_plotly.update_layout(plot_bgcolor="#ECECEC",showlegend=False)
        graph_plotly.update_traces(line_color='#2C2C54')
        return graph_plotly

    @dash_app.callback(
        Output('graph5', 'figure'),
        Input('category5', 'value')
    )
    def plot_data5(category):
        if category == "Total":
            df3[['Date', 'Time']] = df3["Login Datetime"].str.split(' ', expand=True)
            df3[['Year', 'Month', 'Day']] = df3["Date"].str.split('-', expand=True)
            xlabel_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            df3_months = df3.groupby(['Month']).count()
            df3_data2 = df3_months['Time']
            graph_plotly = px.line(df3_months, x=xlabel_month,y=df3_data2,labels={"x":"Months","Time":"User Count"})
            graph_plotly.add_scatter(x=xlabel_month,y=df3_data2)
            graph_plotly.update_layout(plot_bgcolor="#ECECEC",showlegend=False)
            graph_plotly.update_traces(line_color='#2C2C54')
        elif category == "Gender":
            df3[['Date', 'Time']] = df3["Login Datetime"].str.split(' ', expand=True)
            df3[['Year', 'Month', 'Day']] = df3["Date"].str.split('-', expand=True)
            xlabel_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            df3_F = df3.drop(df3[df3["Gender"] == 'M'].index)
            df3_fmonths = df3_F.groupby(['Month']).count()
            df3_fdata = df3_fmonths['Time']
            df3_M = df3.drop(df3[df3["Gender"] == 'F'].index)
            df3_mmonths = df3_M.groupby(['Month']).count()
            df3_mdata = df3_mmonths['Time']
            graph_plotly = px.line(df3_mmonths, x=xlabel_month,y=df3_mdata,labels={"x":"Months","Time":"User Count"})
            graph_plotly.update_layout(plot_bgcolor="#ECECEC")
            graph_plotly.update_traces(line_color='#474787')
            graph_plotly.add_scatter(x=xlabel_month, y=df3_fdata,line_color='#EAB2BB',name="Female")
            graph_plotly.add_scatter(x=xlabel_month, y=df3_mdata,line_color="#474787",name="Male")
        return graph_plotly
    return dash_app
