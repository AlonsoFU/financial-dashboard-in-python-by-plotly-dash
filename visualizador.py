# import individual libraries as in code index.py from folder code
#
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import sqlite3
import webbrowser
import os
from threading import Timer

print("sg")
# Clase para visualizar los datos de la base de datos
class DashBarChart:
    def __init__(self, df_tarjeta_credito, df_cuenta_corriente ,port=8052):
        self.df_tarjeta_credito = df_tarjeta_credito
        self.df_cuenta_corriente = df_cuenta_corriente
        self.port = port

        font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
        meta_tags = [{"name": "viewport", "content": "width=device-width"}]
        external_stylesheets = [meta_tags, font_awesome]

        self.app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

        # df_cuenta_corriente that unique values from Ingreso/pago column
        # Convert Fecha column Fecha to datetime in df_cuenta_corriente where for example in 01/04/23, 01 is day, 04 is month and 23 is year
        df_cuenta_corriente['Fecha'] = pd.to_datetime(df_cuenta_corriente['Fecha'], format='%d/%m/%y') 

        # Convert column Monto to float in df_cuenta_corriente
        df_cuenta_corriente['Monto'] = df_cuenta_corriente['Monto'].str.replace('.', '').astype(float)

        # Convert column Monto to float in df_tarjeta_credito
        df_tarjeta_credito['Monto'] = df_tarjeta_credito['Monto'].str.replace('.', '').astype(float)

        # Convert Fecha column Fecha to datetime in df_tarjeta_credito where for example in 01/04/23, 01 is day, 04 is month and 23 is year
        df_tarjeta_credito['Fecha'] = pd.to_datetime(df_tarjeta_credito['Fecha'], format='%d/%m/%y')

        # Get value group by month and year from column Fecha an column Ingreso/Pago in df_cuenta_corriente over column Monto
        df_cuenta_corriente = df_cuenta_corriente.groupby([df_cuenta_corriente['Fecha'].dt.year.rename('year'), df_cuenta_corriente['Fecha'].dt.month.rename('month'), df_cuenta_corriente['Ingreso/Pago']]).agg({'Monto': 'sum'}).reset_index()


        
        self.app.layout = html.Div([ html.Div([
        html.Div([
            html.Img(src = self.app.get_asset_url('statistics.png'),
                     style = {'height': '30px'},
                     className = 'title_image'
                     ),
            html.H6('Financial Dashboard',
                    style = {'color': '#D35940'},
                    className = 'title'
                    ),
        ], className = 'logo_title'),

        html.Div([
            html.P('Select Month',
                   style = {'color': '#D35940'},
                   className = 'drop_down_list_title'
                   ),
            dcc.Dropdown(id = 'select_month',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Mar',
                         placeholder = 'Select Month',
                         options = [{'label': c, 'value': c}
                                    for c in df_cuenta_corriente['month'].unique()],
                         className = 'drop_down_list'),
        ], className = 'title_drop_down_list'),
    ], className = 'title_and_drop_down_list'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.P('Accounts Receivable',
                               className = 'format_text')
                    ], className = 'accounts_receivable1'),
                    html.Div([
                        html.Div(id = 'accounts_receivable_value',
                                 className = 'numeric_value')
                    ], className = 'accounts_receivable2')
                ], className = 'accounts_receivable_column'),
                html.Div([
                    html.Div([
                        html.P('Accounts Payable',
                               className = 'format_text')
                    ], className = 'accounts_payable1'),
                    html.Div([
                        html.Div(id = 'accounts_payable_value',
                                 className = 'numeric_value')
                    ], className = 'accounts_payable2')
                ], className = 'accounts_payable_column'),
            ], className = 'receivable_payable_column'),

            html.Div([
                html.Div([
                    html.Div([
                        html.P('Income',
                               className = 'format_text')
                    ], className = 'income1'),
                    html.Div([
                        html.Div(id = 'income_value',
                                 className = 'numeric_value')
                    ], className = 'income2')
                ], className = 'income_column'),
                html.Div([
                    html.Div([
                        html.P('Expenses',
                               className = 'format_text')
                    ], className = 'expenses1'),
                    html.Div([
                        html.Div(id = 'expenses_value',
                                 className = 'numeric_value')
                    ], className = 'expenses2')
                ], className = 'expenses_column'),
            ], className = 'income_expenses_column'),
        ], className = 'first_row'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    ], className = 'first_left_circle'),
                    html.Div([
                        html.Div(id = 'second_left_circle'),
                    ], className = 'second_left_circle'),
                ], className = 'first_second_left_column'),
            ], className = 'left_circle_row'),
            dcc.Graph(id = 'chart1',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),
        ], className = 'text_and_chart'),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    ], className = 'first_right_circle'),
                    html.Div([
                        html.Div(id = 'second_right_circle'),
                    ], className = 'second_right_circle'),
                ], className = 'first_second_right_column'),
            ], className = 'right_circle_row'),
            dcc.Graph(id = 'chart2',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),

            html.Div([
                html.Div([
                    html.Div([
                        html.P('Income Statement',
                               className = 'format_text')
                    ], className = 'income_statement'),

                    html.Div([
                        html.Div([
                            html.Div([
                                html.P('Income',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement1',
                                         className = 'income_statement1'),
                            ], className = 'income_statement_indicator_row1'),
                            html.Div([
                                html.P('Cost of Goods Sold',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement2',
                                         className = 'income_statement1')
                            ], className = 'income_statement_indicator_row2'),
                            html.Hr(className = 'bottom_border'),
                            html.Div([
                                html.P('Gross Profit',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement3',
                                         className = 'income_statement1'),
                            ], className = 'income_statement_indicator_row3'),
                            html.Div([
                                html.P('Total Operating Expenses',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement4',
                                         className = 'income_statement1')
                            ], className = 'income_statement_indicator_row4'),
                            html.Hr(className = 'bottom_border'),
                            html.Div([
                                html.P('Operating Profit (EBIT)',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement5',
                                         className = 'income_statement1'),
                            ], className = 'income_statement_indicator_row5'),
                            html.Div([
                                html.P('Taxes',
                                       className = 'income_statement_title'
                                       ),
                                html.Div(id = 'income_statement6',
                                         className = 'income_statement1')
                            ], className = 'income_statement_indicator_row6'),
                        ], className = 'in_state_column')
                    ], className = 'income_statement_multiple_values'),
                ], className = 'income_statement_column1'),
                html.Div([
                    html.Div([
                        html.Div([
                            html.P('Net Profit',
                                   className = 'income_statement_title'
                                   ),
                            html.Div(id = 'income_statement7',
                                     className = 'income_statement1')
                        ], className = 'income_statement_indicator_row7'),
                    ], className = 'net_profit_column')
                ], className = 'net_profit'),
            ], className = 'net_profit1'),
        ], className = 'income_statement_row')
    ], className = 'f_row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.P('Quick Ratio',
                               className = 'format_text')
                    ], className = 'accounts_receivable1'),
                    html.Div([
                        html.Div(id = 'quick_ratio_value',
                                 className = 'numeric_value')
                    ], className = 'accounts_receivable2')
                ], className = 'accounts_receivable_column'),
                html.Div([
                    html.Div([
                        html.P('Current Ratio',
                               className = 'format_text')
                    ], className = 'accounts_payable1'),
                    html.Div([
                        html.Div(id = 'current_ratio_value',
                                 className = 'numeric_value')
                    ], className = 'accounts_payable2')
                ], className = 'accounts_payable_column'),
            ], className = 'receivable_payable_column'),

            html.Div([
                html.Div([
                    html.Div([
                        html.P('Net Profit',
                               className = 'format_text')
                    ], className = 'income1'),
                    html.Div([
                        html.Div(id = 'net_profit_value',
                                 className = 'numeric_value')
                    ], className = 'income2')
                ], className = 'income_column'),
                html.Div([
                    html.Div([
                        html.P('Cash at EOM',
                               className = 'format_text')
                    ], className = 'expenses1'),
                    html.Div([
                        html.Div(id = 'cash_at_eom_value',
                                 className = 'numeric_value')
                    ], className = 'expenses2')
                ], className = 'expenses_column'),
            ], className = 'income_expenses_column'),
        ], className = 'first_row'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    ], className = 'first_left_circle'),
                    html.Div([
                        html.Div(id = 'third_left_circle'),
                    ], className = 'second_left_circle'),
                ], className = 'first_second_left_column'),
            ], className = 'left_circle_row'),
            dcc.Graph(id = 'chart3',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),
        ], className = 'text_and_chart'),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                    ], className = 'first_right_circle'),
                    html.Div([
                        html.Div(id = 'fourth_right_circle'),
                    ], className = 'second_right_circle'),
                ], className = 'first_second_right_column'),
            ], className = 'right_circle_row'),
            dcc.Graph(id = 'chart4',
                      config = {'displayModeBar': False},
                      className = 'donut_chart_size'),

            html.Div([
                dcc.Graph(id = 'bar_chart',
                          config = {'displayModeBar': False},
                          className = 'bar_chart_size'),
            ], className = 'net_profit2'),
        ], className = 'income_statement_row')
    ], className = 'f_row'),

    html.Div([
        dcc.Graph(id = 'line_chart',
                  config = {'displayModeBar': False},
                  className = 'line_chart_size'),
        dcc.Graph(id = 'combination_chart',
                  config = {'displayModeBar': False},
                  className = 'combination_chart_size'),
    ], className = 'last_row')
])


        @self.app.callback(Output('accounts_receivable_value', 'children'),
                    [Input('select_month', 'value')])
        def update_text(select_month):
            if select_month is None:
                raise PreventUpdate
            else:
                filter_month = df_cuenta_corriente[df_cuenta_corriente['months'] == select_month]
                accounts_receivable = filter_month['accounts receivable'].iloc[0]
                pct_accounts_receivable = filter_month['pct_accounts_receivable'].iloc[0]

                if pct_accounts_receivable > 0:
                    return [
                        html.Div([
                            html.P('${0:,.0f}'.format(accounts_receivable),
                                ),
                            html.Div([
                                html.Div([
                                    html.P('+{0:,.1f}%'.format(pct_accounts_receivable),
                                        className = 'indicator1'),
                                    html.Div([
                                        html.I(className = "fas fa-caret-up",
                                            style = {"font-size": "25px",
                                                        'color': '#00B050'},
                                            ),
                                    ], className = 'value_indicator'),
                                ], className = 'value_indicator_row'),
                                html.P('vs previous month',
                                    className = 'vs_previous_month')
                            ], className = 'vs_p_m_column')
                        ], className = 'indicator_column'),
                    ]
                elif pct_accounts_receivable < 0:
                    return [
                        html.Div([
                            html.P('${0:,.0f}'.format(accounts_receivable),
                                ),
                            html.Div([
                                html.Div([
                                    html.P('{0:,.1f}%'.format(pct_accounts_receivable),
                                        className = 'indicator2'),
                                    html.Div([
                                        html.I(className = "fas fa-caret-down",
                                            style = {"font-size": "25px",
                                                        'color': '#FF3399'},
                                            ),
                                    ], className = 'value_indicator'),
                                ], className = 'value_indicator_row'),
                                html.P('vs previous month',
                                    className = 'vs_previous_month')
                            ], className = 'vs_p_m_column')
                        ], className = 'indicator_column'),
                    ]
                elif pct_accounts_receivable == 0:
                    return [
                        html.Div([
                            html.P('${0:,.0f}'.format(accounts_receivable),
                                ),
                            html.Div([
                                html.Div([
                                    html.P('{0:,.1f}%'.format(pct_accounts_receivable),
                                        className = 'indicator2'),
                                ], className = 'value_indicator_row'),
                                html.P('vs previous month',
                                    className = 'vs_previous_month')
                            ], className = 'vs_p_m_column')
                        ], className = 'indicator_column'),
                    ]

    def open_browser(self):
            # Abre el navegador web para visualizar la aplicación
            debug_mode = self.app.server.debug
            run_main = os.environ.get
            ("WERKZEUG_RUN_MAIN") == "true"
            if not debug_mode or run_main:
                webbrowser.get("firefox").open_new(f"http://localhost:{self.port}")

    def run(self):
            # Inicia la aplicación Dash y abre el navegador
            Timer(1, self.open_browser).start()
            self.app.run_server(debug=False, port=self.port)

print("sg")