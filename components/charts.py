"""Plotly chart wrappers for ZPOTS."""
import plotly.graph_objects as go


ZPOTS_LIME = "#cffc00"
ZPOTS_LIME_DIM = "#a8d600"
ZPOTS_PRIMARY = "#506300"
ZPOTS_SURFACE = "#f6f6ff"
ZPOTS_ON_SURFACE = "#272e42"
ZPOTS_OUTLINE = "#a5adc6"


def _base_layout(**overrides):
    layout = dict(
        font=dict(family="Inter, sans-serif", color=ZPOTS_ON_SURFACE),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=40),
        height=280,
        showlegend=False,
    )
    layout.update(overrides)
    return layout


def utilization_bar_chart(data: dict, height=280):
    """Bar chart for weekly utilization (Mon-Sun)."""
    days = list(data.keys())
    values = list(data.values())
    colors = [ZPOTS_LIME if v > 75 else ZPOTS_LIME_DIM for v in values]

    fig = go.Figure(data=[
        go.Bar(x=days, y=values, marker_color=colors, marker_line_width=0, width=0.6)
    ])
    fig.update_layout(**_base_layout(
        height=height,
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(165,173,198,0.15)", showline=False, range=[0, 100]),
    ))
    return fig


def pricing_elasticity_chart(height=250):
    """Bar chart for pricing elasticity (Mon-Sun)."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    values = [420, 380, 450, 510, 680, 620, 350]
    colors = [ZPOTS_LIME if v > 500 else ZPOTS_LIME_DIM for v in values]

    fig = go.Figure(data=[
        go.Bar(x=days, y=values, marker_color=colors, marker_line_width=0, width=0.5)
    ])
    fig.update_layout(**_base_layout(
        height=height,
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(165,173,198,0.15)", showline=False),
    ))
    return fig


def peak_utilization_chart(height=200):
    """Vertical bar chart for peak utilization hours."""
    hours = ["6AM", "9AM", "12PM", "3PM", "6PM", "9PM"]
    values = [20, 45, 60, 55, 95, 70]
    colors = [ZPOTS_LIME if v > 80 else ZPOTS_LIME_DIM for v in values]

    fig = go.Figure(data=[
        go.Bar(x=hours, y=values, marker_color=colors, marker_line_width=0, width=0.5)
    ])
    fig.update_layout(**_base_layout(
        height=height,
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=False, showline=False, visible=False),
    ))
    return fig


def demand_radar_chart(district_data, height=300):
    """Radar/spider chart for district demand."""
    categories = [d["name"] for d in district_data]
    values = [d["demand"] for d in district_data]
    # Close the polygon
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure(data=[
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(207,252,0,0.2)',
            line=dict(color=ZPOTS_LIME, width=2),
            marker=dict(size=6, color=ZPOTS_LIME),
        )
    ])
    fig.update_layout(**_base_layout(
        height=height,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], showline=False, gridcolor="rgba(165,173,198,0.2)"),
            angularaxis=dict(gridcolor="rgba(165,173,198,0.2)"),
        ),
    ))
    return fig


def mini_bar_chart(values, height=80):
    """Tiny bar chart for inline use."""
    fig = go.Figure(data=[
        go.Bar(x=list(range(len(values))), y=values, marker_color=ZPOTS_LIME, marker_line_width=0, width=0.6)
    ])
    fig.update_layout(**_base_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    ))
    return fig
