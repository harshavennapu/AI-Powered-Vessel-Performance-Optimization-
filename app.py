import plotly.express as px
import streamlit as st
import pandas as pd
st.sidebar.title("🚢 Navigation")
st.caption("AI Powered Vessel Performance Monitoring System")

st.sidebar.info("""
Vessel Optimization Dashboard

Features:
- Voyage KPIs
- Fuel Analysis
- Performance Tracking
- Weather Monitoring
""")

st.set_page_config(
    page_title="Vessel Optimization Tool",
    layout="wide"
)

st.title("🚢 Vessel Optimization Tool")

uploaded_file = st.file_uploader(
    "Upload Noon Report Excel",
    type=["xlsx"]
)

if uploaded_file:

    # Read Excel
    df = pd.read_excel(uploaded_file)

    st.subheader("View Raw Noon Report Data")
    st.dataframe(df)

    # -----------------------------------
    # FUNCTION TO EXTRACT VALUES
    # -----------------------------------

    def get_value(keyword):

        search_col=df.iloc[:,1].astype(str).str.upper()
        row = df[df.iloc[:,1].astype(str).str.contains(
            keyword.upper(),
            na=False
        )]

        if not row.empty:
            value=row.iloc[0,2]
            if pd.isna(value):
                return "No Data"
            return value

        return "Not Available"

    # -----------------------------------
    # EXTRACT KPIs
    # -----------------------------------

    avg_speed = get_value("AVG SPEED")
    cp_speed = get_value("ALLOWED CP SPEED")
    distance = get_value("DISTANCE SAILED")
    wind_speed = get_value("WIND SPEED")

    total_hsfo = get_value("CYL")
    total_lsfo = get_value("SYSTEM")

    rob_hsfo = get_value("ROB")
    rob_lsfo = get_value("SYSTEM OIL ROB")

    # -----------------------------------
    # KPI DASHBOARD
    # -----------------------------------

    st.subheader("Voyage KPIs")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Speed", avg_speed)
    col2.metric("CP Allowed Speed", cp_speed)
    col3.metric("Distance Sailed", distance)
    col4.metric("Wind Speed", wind_speed)

    # -----------------------------------
    # FUEL CONSUMPTION
    # -----------------------------------

    st.subheader("Fuel Consumption")

    col5, col6 = st.columns(2)

    col5.metric("HSFO Consumption", total_hsfo)
    col6.metric("LSFO Consumption", total_lsfo)

    # -----------------------------------
    # ROB SECTION
    # -----------------------------------

    st.subheader("Remaining On Board (ROB)")

    col7, col8 = st.columns(2)

    col7.metric("ROB HSFO", rob_hsfo)
    col8.metric("ROB LSFO", rob_lsfo)

    # -----------------------------------
    # PERFORMANCE ANALYSIS
    # -----------------------------------

    st.subheader("Performance Analysis")

    try:

        speed_variance = float(avg_speed) - float(cp_speed)

        if speed_variance >= 0:

            st.success(
                f"Vessel is ABOVE CP speed by {speed_variance:.2f} knots"
            )

        else:

            st.error(
                f"Vessel is BELOW CP speed by {abs(speed_variance):.2f} knots"
            )

    except:

        st.warning("Unable to calculate speed variance")
    # -----------------------------------
    # PERFORMANCE SCORE
    # -----------------------------------

    st.subheader("Performance Score")
    try:
        score = (float(avg_speed) / float(cp_speed)) * 100

        st.progress(int(score))

        st.write(f"Efficiency Score: {score:.1f}%")

    except:

        st.warning("Unable to calculate performance score")

    # -----------------------------------
    # CHARTS
    # -----------------------------------

    st.subheader("Performance Charts")

    chart_data = pd.DataFrame({
        "Metric": [
        "Avg Speed",
        "CP Speed",
        "Wind Speed"
        ],
        "Value": [
            float(avg_speed),
            float(cp_speed),
            float(wind_speed)
       ]
    })

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Value",
        title="Voyage Performance Overview"
        )
    st.plotly_chart(fig, use_container_width=True)
    # -----------------------------------
    # WEATHER ANALYSIS
    # -----------------------------------

    st.subheader("Weather Condition Analysis")

    try:
        if float(wind_speed) > 15:
            st.warning("⚠ High wind conditions detected")

        else:

            st.success("✅ Weather conditions are stable")

    except:

        st.warning("No weather data available")
    st.markdown("---")
    st.caption("Developed for Maritime Vessel Performance Optimization")
    # =========================
    # RAW DATA
    # =========================

    with st.expander("View Raw Noon Report Data"):
        st.dataframe(df)
    
    # =========================
    # DOWNLOAD REPORT
    # =========================

    kpi_df = pd.DataFrame([{
        "Avg Speed": avg_speed,
        "CP Speed": cp_speed,
        "Distance Sailed": distance,
        "Wind Speed": wind_speed,
        "HSFO Consumption": total_hsfo,
        "LSFO Consumption": total_lsfo,
        "ROB HSFO": rob_hsfo,
        "ROB LSFO": rob_lsfo
    }])

    st.download_button(
        label="Download KPI Report",
        data=kpi_df.to_csv(index=False),
        file_name="voyage_kpis.csv",
        mime="text/csv"
    )
