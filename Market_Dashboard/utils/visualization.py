# utils/visualization.py

import plotly.express as px

def line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y, title=title)
    return fig

def scatter_chart(df, x, y, color, title):
    fig = px.scatter(df, x=x, y=y, color=color, title=title)
    return fig

def bar_chart(df, x, y, title):
    fig = px.bar(df, x=x, y=y, title=title)
    return fig
