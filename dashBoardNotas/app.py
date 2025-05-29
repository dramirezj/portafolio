import dash
from dash import html,dcc,Input,Output
import pandas as pd
import plotly.express as px

#cargar datos
fdatos = pd.read_csv("notas_limpias.csv")

#Crear la aplicacion 
app = dash.Dash(__name__)
server = app.server
app.title = "DashBoard Notas Estudiantes"

#crear ventana del dashboard
app.layout = html.Div([
    html.H1("DashBoard Notas por Estudiante", style={"text-align":"center"}),
    html.Label("Seleccione una carrera: "),
    dcc.Dropdown (
                id="career",
                options=[{"label":g,"value":g} for g in fdatos["Carrera"].unique()],
                value=fdatos["Carrera"].unique()[0],
                clearable=False
            ),
    html.Br(),
    dcc.Tabs(children=[
        dcc.Tab(label="Grafico Promedios",children=[
            dcc.Tab(dcc.Graph(id="grafico-histograma"))
        ]),
        dcc.Tab(label="Grafico Edad vs Promedio",children=[
            dcc.Tab(dcc.Graph(id="grafico-dispersion"))
        ]),
        dcc.Tab(label="Grafico Desempeño",children=[
            dcc.Tab(dcc.Graph(id="grafico-pie"))
        ]),
        dcc.Tab(label="Grafico Promedio Notas por Carrera",children=[
            dcc.Tab(dcc.Graph(id="grafico-bar"))
        ]),
    ]),
])

#actualizar grafico
@app.callback(Output("grafico-histograma","figure"),
              Output("grafico-dispersion","figure"),
              Output("grafico-pie","figure"),
              Output("grafico-bar","figure"),
              Input("career","value"))

def actualizar(career):
    filtro = fdatos[fdatos["Carrera"]==career]
    hist = px.histogram(
        filtro,
        x="Promedio",
        color="Promedio",
        nbins=10,
        title=f"Distribución Promedio Notas - {career}"
    )
    scatter = px.scatter(
        filtro,
        x="Edad",
        y="Promedio",
        color="Desempeño",
        title=f"Edad vs Promedio - {career}"
    )
    promedios = fdatos.groupby("Carrera")["Promedio"].mean().reset_index()
    pie = px.pie(filtro,
                 names = "Desempeño",
                 title = f"Desempeño por Carrera - {career}")
    bar = px.bar(promedios,
                 x = "Carrera",
                 y = "Promedio",
                 color="Carrera",
                 color_discrete_sequence=px.colors.qualitative.Dark2,
                 title = f"Promedio por Carrera - {career}")
    
    
    return hist,scatter,pie,bar

#ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)