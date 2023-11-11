# 1. Import Library
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


### Import data disini
paxel_palette = ['#ffc107', '#fd7e14', '#dc3545', '#e83e8c', '#6f42c1']

record = pd.read_pickle('data_input/shipping_record')
record = record.stack().reset_index()

# --------------------------- CARD --------------------------------------
### Info card disini

# Menghitung Total Pengiriman Berhasil
Total_Pengiriman_Berhasil = f"{record['Completed'].sum():,.0f}"

# Menghitung Total Pengiriman Cancelled
Total_Pengiriman_Cancelled = f"{record['Cancelled'].sum():,.0f}"

# Menghitung Total Pengiriman Delivery fail
Total_Pengiriman_Delivery_fail = f"{record['Delivery fail'].sum():,.0f}"

# Menghitung Total Pengiriman On Hold
Total_Pengiriman_On_Hold = f"{record['On Hold'].sum():,.0f}"

# Menghitung Total Pengiriman Transit
Total_Pengiriman_Transit = f"{record['Transit'].sum():,.0f}"

card_Total_Pengiriman_Berhasil = [
    dbc.CardHeader("Total Pengiriman Berhasil",
                   style={'color': '#5f4fa0',
                        'font-size':'30px'}),
    dbc.CardBody(
        [
            html.H1(Total_Pengiriman_Berhasil, style={'color': '#5f4fa0',
                                                      'font-size':'30px'}),
        ]
    ),
]

card_Total_Pengiriman_Cancelled = [
    dbc.CardHeader("Total Pengiriman Cancelled",
                   style={'color': '#ffb200',
                        'font-size':'30px'}),
    dbc.CardBody(
        [
            html.H1(Total_Pengiriman_Cancelled, style={'color': '#ffb200',
                                                       'font-size':'30px'}),
        ]
    ),
]

card_Total_Pengiriman_Delivery_fail = [
    dbc.CardHeader("Total Pengiriman Delivery Fail",
                   style={'color': '#ff434f',
                        'font-size':'30px'}),
    dbc.CardBody(
        [
            html.H1(Total_Pengiriman_Delivery_fail, style={'color': '#ff434f',
                                                           'font-size':'30px'}),
        ]
    ),
]

card_Total_Pengiriman_On_Hold = [
    dbc.CardHeader("Total Pengiriman On Hold",
                   style={'color': '#5f4fa0',
                        'font-size':'30px'}),
    dbc.CardBody(
        [
            html.H1(Total_Pengiriman_On_Hold, style={'color': '#5f4fa0',
                                                     'font-size':'30px'}),
        ]
    ),
]

card_Total_Pengiriman_Transit = [
    dbc.CardHeader("Total Pengiriman Transit",
                   style={'color': '#5f4fa0',
                        'font-size':'30px'}),
    dbc.CardBody(
        [
            html.H1(Total_Pengiriman_Transit, style={'color': '#5f4fa0',
                                                     'font-size':'30px'}),
        ]
    ),
]

# ------------------------Linechart 1--------------------------------------
fig_line_all = px.line(
            record, 
            x='creation_date',
            y=record.drop(['creation_date', 'ship_mode'], axis=1).sum(axis=1),
            color='ship_mode', 
            title='Tren Jumlah Pengiriman Keseluruhan',
            color_discrete_sequence=['#dc3545', '#e83e8c', '#6f42c1'],
            template='plotly_white',
            hover_name='ship_mode',
            labels={
                'creation_date': 'Tanggal Pengiriman',
                'y':'Jumlah Pengiriman',
                'ship_mode':'Mode Pengiriman'
            }
)

# ------------------------linechart 2--------------------------------------
fiq_line = px.line(
    record, 
    x='creation_date', 
    y=record['Delivery fail'],
    color_discrete_sequence=['#6f42c1'],
    template='plotly_white',
    labels={
        'creation_date': 'Tanggal Pengiriman'
    }, 
    title='Tren Jumlah Pengiriman yang Gagal')
fig_line = fiq_line.update_layout(
                yaxis=dict(
                    tickvals=[0, 1],
                    ticktext=['0', '1']
                )
)

#-------------------------Donut Chart------------------------------------------
fig_donut = px.pie(
    record, 
    names='ship_mode', 
    values='Completed', 
    title='Persentase Pengiriman Selesai (Completed) Berdasarkan Tipe Pengiriman',
    hole=0.4,
    color_discrete_sequence=['#6f42c1', '#e83e8c', '#ffc107'],
    template='plotly_white',
    labels={
        'creation_date': 'Tanggal Pengiriman',
        'ship_mode':'Mode Pengiriman'},
    )


# 2. Create Dashboard Instance-----------------------------------

app = Dash(
    external_stylesheets=[dbc.themes.PULSE],
    name='Dashboard - Pengiriman'
    )

server=app.server

app.title = 'Dashboard - Pengiriman'

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),        
    ],
    brand="Dashboard Pengiriman",
    brand_href="#",
    color="#5f4fa0",   
    dark=True,
)

# ----------------------------USER INTERFACE----------------------------------
## Kode untuk menampilkan apapun di halaman website
app.layout = html.Div(children=[
    navbar,
    html.Br(),
    
    html.Div(
        [
            ## ---------- ROW 1 --------
            dbc.Row(
                [
                    ## ---- COL 1 -----
                    dbc.Col(
                        [   
                            dbc.Card(
                                card_Total_Pengiriman_Berhasil,
                                color='white'
                            ),
                            html.Br(),
                            dbc.Card(
                                card_Total_Pengiriman_Transit,
                                color='white'
                            ),
                            html.Br(),
                            dbc.Card(
                                card_Total_Pengiriman_On_Hold,
                                color='white'
                            ),
                            html.Br(),
                            dbc.Card(
                                card_Total_Pengiriman_Cancelled,
                                color='white'
                            ),
                             html.Br(),
                            dbc.Card(
                                card_Total_Pengiriman_Delivery_fail,
                                color='white'
                            ),
                        ],width=3,
                    ),
                    ## ----- COL 2 ----
                    dbc.Col(
                        [
                            dcc.Graph(figure = fig_line_all,
                                                    style= {
                                                #'width': '400px',
                                                'height': '825px'},
                                      ),
                        ]
                    ),
                ]
            ),
                                                               
            ##---ROW 2----------------------------------------------
            dbc.Row(
               [
                  html.H1("Analisa Pengiriman Berdasarkan Status", style={'text-align':'center',
                                                                'background-color': '#5e50a1',
                                                               'color':'white',
                                                               'font-size':'20px'
                                                               }),
            ## ------ Row 2 Col 1 --------
            dbc.Col(
               [
                  dcc.Graph(figure = fig_donut),       
               ],width=6
            ),

            ## ------ Row 2 Col 2 --------
            dbc.Col(
               [
                  dcc.Graph(figure = fig_line),
               ]
           # ,style={'background-color':'#5e50a1', 'opacity':1,}
                    ),
               ]
            ),
        ]
    ),
],style={
    'background-color':'#fff', 'opacity':1,
    'padding-right':'30px',
    'padding-left':'30px',
    'padding-bottom': '30px'
}
)

# 3. Start the Dash Server
if __name__ == '__main__':
   app.run(debug=True)
