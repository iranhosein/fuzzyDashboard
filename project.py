import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# ---------- مدل عدد فازی ----------
class TriangularFuzzyNumber:
    def __init__(self, left, middle, right):
        self.a = left
        self.b = middle
        self.c = right

    def __mul__(self, other):
        if (self.b > 0 and other.b > 0):
            a = self.b * other.a + other.b * self.a
            b = self.b * other.b
            c = self.b * other.c + other.b * self.c
        elif (self.b < 0 and other.b > 0):
            a = other.b * self.a - self.b * other.c
            b = self.b * other.b
            c = other.b * self.c - self.b * other.a
        else:
            a = (-1) * other.b * self.c - self.b * other.c
            b = self.b * other.b
            c = (-1) * other.b * self.a - self.b * other.a
        return TriangularFuzzyNumber(a, b, c)

    def get_coords(self):
        return [self.a, self.b, self.c], [0, 1, 0]

# ---------- اپ ----------
app = dash.Dash(__name__)
app.title = "ضرب اعداد فازی"

# ---------- ظاهر داشبورد ----------
app.layout = html.Div(
    style={
        'fontFamily': 'Vazir, sans-serif',
        'backgroundColor': '#1e1e2f',
        'color': 'white',
        'padding': '40px',
        'textAlign': 'center',
    },
    children=[
        html.H1("🧠 ابزار ضرب اعداد فازی", style={'fontSize': '36px', 'marginBottom': '30px'}),

        html.Div([
            html.Div([
                html.H3("عدد فازی اول"),
                dcc.Input(id='a1', type='number', value=1, step=0.1, placeholder='a1',
                          style={'margin': '5px'}),
                dcc.Input(id='b1', type='number', value=2, step=0.1, placeholder='b1',
                          style={'margin': '5px'}),
                dcc.Input(id='c1', type='number', value=3, step=0.1, placeholder='c1',
                          style={'margin': '5px'}),
            ], style={'width': '45%', 'display': 'inline-block'}),

            html.Div([
                html.H3("عدد فازی دوم"),
                dcc.Input(id='a2', type='number', value=2, step=0.1, placeholder='a2',
                          style={'margin': '5px'}),
                dcc.Input(id='b2', type='number', value=3, step=0.1, placeholder='b2',
                          style={'margin': '5px'}),
                dcc.Input(id='c2', type='number', value=4, step=0.1, placeholder='c2',
                          style={'margin': '5px'}),
            ], style={'width': '45%', 'display': 'inline-block'}),
        ], style={'marginBottom': '40px'}),

        html.Div([
            dcc.Graph(id='output-graph', config={
                'toImageButtonOptions': {'format': 'png'},
                'displaylogo': False,
                'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d']
            })
        ])
    ]
)

# ---------- کالبک خروجی ----------
@app.callback(
    Output('output-graph', 'figure'),
    Input('a1', 'value'), Input('b1', 'value'), Input('c1', 'value'),
    Input('a2', 'value'), Input('b2', 'value'), Input('c2', 'value'),
)
def update_graph(a1, b1, c1, a2, b2, c2):
    f1 = TriangularFuzzyNumber(a1, b1, c1)
    f2 = TriangularFuzzyNumber(a2, b2, c2)
    result = f1 * f2

    x1, y1 = f1.get_coords()
    x2, y2 = f2.get_coords()
    x3, y3 = result.get_coords()

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x1, y=y1, mode='lines+markers', name='عدد اول', line=dict(color='cyan', width=3)))
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines+markers', name='عدد دوم', line=dict(color='orange', width=3)))
    fig.add_trace(go.Scatter(x=x3, y=y3, mode='lines+markers', name='نتیجه ضرب', line=dict(color='lime', width=4, dash='dot')))

    fig.update_layout(
        plot_bgcolor='#111',
        paper_bgcolor='#1e1e2f',
        font_color='white',
        title='ضرب عددهای فازی مثلثی',
        xaxis_title='مقدار',
        yaxis_title='درجه عضویت',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )

    return fig

# ---------- اجرا ----------
if __name__ == '__main__':
    app.run(debug=True)
