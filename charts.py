import plotly.express as px
import pandas as pd


def create_performance_chart(kpis):

    chart_data = pd.DataFrame({
        "Metric": [
            "Avg Speed",
            "CP Speed",
            "Wind Speed"
        ],
        "Value": [
            float(kpis.get("avg_speed") or 0),
            float(kpis.get("cp_speed") or 0),
            float(kpis.get("wind_speed") or 0)
        ]
    })

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Value",
        title="Voyage Performance Overview"
    )

    return fig