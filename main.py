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
# import time to use Timer
from threading import Timer
import visualizador as vs

# Connect with database in /home/alonso/Documentos/Datos_Proyecto/Finanzas.db
conn = sqlite3.connect('/home/alonso/Documentos/Datos_Proyecto/Finanzas.db')
# df cuebta corriente
df_cuenta_corriente = pd.read_sql_query("SELECT * FROM Corriente", conn)
# df tarjeta de credito
df_tarjeta_credito = pd.read_sql_query("SELECT * FROM Tarjeta", conn)
print(df_cuenta_corriente)

# Run app

vs.DashBarChart(df_tarjeta_credito, df_cuenta_corriente).run()