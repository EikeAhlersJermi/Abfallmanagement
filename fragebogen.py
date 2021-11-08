from re import template
import pandas as pd
import plotly  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go
import datetime
import numpy as np
#import locale
#locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Lebensmittelabfall Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="Lebensmittelabfall.xlsx",
        engine="openpyxl",
        sheet_name="Abfalldokumentation",
  #      skiprows=0,
        usecols="A:V",
  #      nrows=1000,
    )
    # Add 'hour' column to dataframe
    
    df['date'] = df['Datum'].dt.date

    return df

df = get_data_from_excel()




# ---- MAINPAGE ----

st.title(":bar_chart: Lebensmittelabfall Dashboard")
st.markdown("##")

Menge_Lebensmittelabfall = int(df["Menge"].sum())

Entsorgungskosten = Menge_Lebensmittelabfall * 0.13 

st.subheader(f"Menge Lebensmittelabfall: {Menge_Lebensmittelabfall:n} kg")