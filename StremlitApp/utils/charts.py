import plotly.express as px
from utils.constants import MODEL_COLORS

def line_chart(df, title):
    """
    Generic line chart for forecast data
    """
    fig = px.line(
        df,
        x="date",
        y="forecast_price",
        color="model",
        markers=True,
        title=title,
        color_discrete_map=MODEL_COLORS,
        template="plotly_dark"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        legend_title="Model"
    )
    return fig


def single_model_chart(df, model, title):
    """
    Line chart for a single model
    """
    fig = px.line(
        df,
        x="date",
        y="forecast_price",
        markers=True,
        title=title,
        color_discrete_sequence=[MODEL_COLORS.get(model, "#ffffff")],
        template="plotly_dark"
    )

    fig.update_layout(
        height=350,
        xaxis_title="Date",
        yaxis_title="Price (USD)"
    )
    return fig
