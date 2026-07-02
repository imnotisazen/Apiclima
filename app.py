import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Consulta del Clima",
    page_icon="🌤️",
    layout="centered"
)

st.title("App del Clima")

ciudades = {
    "Tegucigalpa": (14.0723, -87.1921),
    "San Pedro Sula": (15.5042, -88.0250),
    "La Ceiba": (15.7597, -86.7822),
    "Choluteca": (13.3017, -87.1908),
    "Comayagua": (14.4528, -87.6376)
}

ciudad = st.selectbox("Seleccione una ciudad", list(ciudades.keys()))

latitud, longitud = ciudades[ciudad]

url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitud}&longitude={longitud}"
    f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    f"&hourly=temperature_2m"
    f"&forecast_days=1"
)

respuesta = requests.get(url)

if respuesta.status_code == 200:

    datos = respuesta.json()

    actual = datos["current"]

    st.header(f"Clima actual en {ciudad}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Temperatura",
            f"{actual['temperature_2m']} °C"
        )

    with col2:
        st.metric(
            "Humedad",
            f"{actual['relative_humidity_2m']} %"
        )

    with col3:
        st.metric(
            "Velocidad del viento",
            f"{actual['wind_speed_10m']} km/h"
        )

    st.divider()

    st.subheader("Pronóstico de temperatura")

    # Obtener únicamente la hora (HH:MM)
    horas = [hora.split("T")[1] for hora in datos["hourly"]["time"]]
    temperaturas = datos["hourly"]["temperature_2m"]

    df = pd.DataFrame({
        "Hora": horas,
        "Temperatura (°C)": temperaturas
    })

    # Gráfico
    st.line_chart(df.set_index("Hora"))

    st.subheader("Datos del pronóstico")

    # Tabla
    st.dataframe(df, use_container_width=True)

else:
    st.error("No fue posible obtener los datos del clima.")