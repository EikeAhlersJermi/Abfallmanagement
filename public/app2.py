# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Lebensmittelabfall Dashboard w/ Streamlit



from re import template
import pandas as pd
import plotly  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go
import datetime
import numpy as np



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
        usecols="A:L",
  #      nrows=1000,
    )
    # Add 'hour' column to dataframe
    
    df['date'] = df['Datum'].dt.date

    return df

def get_data_from_excel2():
    df_kennzahlen = pd.read_excel(
        io="Lebensmittelabfall.xlsx",
        engine="openpyxl",
        sheet_name="Kennzahlen",
       # usecols="A:H",
    )
    
    return df_kennzahlen



df = get_data_from_excel()


df_kennzahlen = get_data_from_excel2()

today = datetime.date.today()

# ---- SIDEBAR ----
#Zeitraumfilter
date = st.sidebar.date_input('Startdatum', datetime.date(2021,9,1))
date2 = st.sidebar.date_input('Enddatum', today)
mask = (df['date'] >= date) & (df['date'] <= date2)
df = df.loc[mask]

zeitraum=date2-date+datetime.timedelta(days=1)

weekNumber_start = date.isocalendar()[1]
weekNumber_end = date2.isocalendar()[1]
mask2 = (df_kennzahlen['KW'] >= weekNumber_start) & (df_kennzahlen['KW'] <= weekNumber_end)
df_kennzahlen = df_kennzahlen.loc[mask2]

st.sidebar.write('Zeitraum: ',zeitraum)
st.sidebar.write("KW ", weekNumber_start, " - ", " KW " , weekNumber_end)   



BU = st.sidebar.multiselect(
    "Filter der BUs:",
    options=df["BU"].unique(),
    default=df["BU"].unique()
)
Symptom = st.sidebar.multiselect(
    "Wähle das Symptom aus:",
    options=df["Symptom"].unique(),
    default=df["Symptom"].unique(),
)
Grund = st.sidebar.multiselect(
    "Filter zum genauen Grund:",
    options=df["Grund"].unique(),
    default=df["Grund"].unique()
)

KW = st.sidebar.multiselect(
    "Auswahl der KW:",
    options=df_kennzahlen["KW"].unique(),
    default=df_kennzahlen["KW"].unique()
)



df_selection = df.query(
   "BU == @BU & Symptom ==@Symptom & Grund == @Grund"
   
)
# converting the date to the required format
df['date'] = pd.to_datetime(df['date'], errors ='coerce')
#df['date'].astype('int64').dtypes




df_selection_kennzahlen = df_kennzahlen.query(
   "BU == @BU & KW ==@KW"
)
#Sunburst Gründe
#Definition Variable
a = df_selection["BU"]
b = df_selection["Symptom"]
c = df_selection["Grund"]
d = df_selection["Produktgruppe"]
e = df_selection["Produktname"]
f = df_selection["Datum"]
g = df_selection["genauer Grund"]
z = df_selection["filter_a"]
zz = df_selection["filter_b"]
zzz = df_selection["filter_c"]

menge = df_selection["Menge"]

df_sunburst = pd.DataFrame(
    dict(a=a, b=b, c=c, d=d , e=e ,f=f, g=g , z=z , zz=zz , zzz=zzz ,menge=menge)
)



df_sunburst = pd.DataFrame(
    dict(a=a, b=b, c=c, d=d , e=e ,f=f, g=g , z=z , zz=zz , zzz=zzz ,menge=menge)
)

gesamt_grund = px.sunburst(df_sunburst, path=['z', 'b', 'c','g','d','e','f'], values="menge",


maxdepth=2
)
gesamt_grund.update_traces(textinfo='label+percent entry',textfont_size=20,  hovertemplate=' %{value} kg',)
gesamt_grund.update_layout(
    margin=dict(l=20, r=350, t=40, b=40),
    separators=",."
)


bu_grund = px.sunburst(df_sunburst, path=['zz', 'a', 'd', 'e' , 'g'], values="menge",
color="a",
    color_discrete_map={
        "BU1":"#EF553B",
        "BU2":"#FFA15A",
        "BU3":"#636EFA",
        "BU4":"#AB63FA", 
        "Verkauf":'#90ee90',
        "Rest": '#808080'
    },

maxdepth=2

)
bu_grund.update_traces(textinfo='label+percent entry',textfont_size=20,hovertemplate=' %{value} kg')
bu_grund.update_layout(
    margin=dict(l=20, r=350, t=40, b=40),
    separators=",."
)

produkte = px.sunburst(df_sunburst, path=['zzz', 'd','e', 'b','c','f'], values="menge",

maxdepth=2
)
produkte.update_traces(textinfo='label+percent entry',textfont_size=20, hovertemplate='%{value} kg',)
produkte.update_layout(
    margin=dict(l=20, r=350, t=40, b=40),
    separators=",."
)

treemap = px.treemap(df_sunburst, path=['a', 'd','b','e','f'], values="menge",
color="a",
    color_discrete_map={
        "BU1":"#EF553B",
        "BU2":"#FFA15A",
        "BU3":"#636EFA",
        "BU4":"#AB63FA", 
        "Verkauf":'#90ee90',
        "Rest": '#808080'
    },
maxdepth=3, height=1000, width=1300
)

treemap.update_traces(textinfo='label+percent entry',textfont_size=20, hovertemplate='Menge %{value} kg <br>Prozent Gesamt %{percentRoot:.2f}',)
treemap.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    separators=",.",
    
)



# treemap = px.treemap(df_selection, path=[px.Constant(""), 'BU', 'Symptom', 'Grund', 'Produktgruppe'],branchvalues="total", values='Menge',color="Symptom",maxdepth=2,
    
# )
# #treemap.data[0].textinfo = 'label+text+percent entry' 

# treemap.update_layout(
#     margin = dict(t=50, l=25, r=25, b=25),
#     separators=",.", 
    
    
#     )
# treemap.update_traces(
#     textfont_size=20,
#     textinfo='label+percent entry'
# )

# treemap.data[0].hovertemplate = '%{value} kg <br>%{percentRoot} '






# TOP KPI's

Menge_Lebensmittelabfall = int(df_selection["Menge"].sum())


# Gesamtlebensmittelabfallquote [BAR CHART]
gesamtlebensmittelabfall = (
    df_selection_kennzahlen.groupby(by=["KW"]).sum()[["Gesamtlebensmittelabfallquote"]].sort_values(by="Gesamtlebensmittelabfallquote")
)
gesamtlebensmittelabfall = px.bar(
    df_selection_kennzahlen,    
    x="KW",
    y="Gesamtlebensmittelabfallquote",   
    color="BU",
    color_discrete_map={
        "BU1":"#EF553B",
        "BU2":"#FFA15A",
        "BU3":"#636EFA",
        "BU4":"#AB63FA",    
    }
    
    
    ,
    barmode='group',
    template="plotly_white",
    
)
gesamtlebensmittelabfall.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    separators=",."
)
gesamtlebensmittelabfall.update_traces(    
    selector=dict(type='bar'),
    hovertemplate=' %{value} %',
    texttemplate='%{value:.2f}',
    textposition='outside'
   
)
# Maschinenabfallquote [BAR CHART]
maschinenabfall = (
    df_selection_kennzahlen.groupby(by=["KW"]).sum()[["Maschinenabfallquote"]].sort_values(by="Maschinenabfallquote")
)
maschinenabfall = px.bar(
    df_selection_kennzahlen,    
    x="KW",
    y="Maschinenabfallquote", 
    color="BU",
    color_discrete_map={
        "BU1":"#EF553B",
        "BU2":"#FFA15A",
        "BU3":"#636EFA",
        "BU4":"#AB63FA",    
    },
    barmode='group',
    #color_discrete_sequence=["#0083B8"] * len(maschinenabfall),
    template="plotly_white",
)
maschinenabfall.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    separators=",.",
)
maschinenabfall.update_traces(    
    selector=dict(type='bar'),
    hovertemplate=' %{value} %',
    texttemplate='%{value:.2f}',
    textposition='outside'
)


# zeitlicher Verlauf [BAR CHART]
verlauf = (
    df_selection.groupby(by=["KW"]).sum()[["Menge"]].sort_values(by="Menge")
)
verlauf = px.bar(
    verlauf,    
    x=verlauf.index,
    y="Menge",
    color_discrete_sequence=["#0083B8"] * len(verlauf),
    template="plotly_white",
)
verlauf.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    separators=",."
    
)
verlauf.update_traces(    
    selector=dict(type='bar'),
    hovertemplate=' %{value} kg',
    texttemplate='%{value}',
    textposition='outside',
)


# Lebensmittelabfall BY Symptom [BAR CHART]
Lebensmittelabfall_by_product_line = (
    df_selection.groupby(by=["Symptom"]).sum()[["Menge"]].sort_values(by="Menge")
)
fig_product_Lebensmittelabfall = px.bar(
    Lebensmittelabfall_by_product_line,
    x="Menge",
    y=Lebensmittelabfall_by_product_line.index,
    orientation="h",
    
    color_discrete_sequence=["#0083B8"] * len(Lebensmittelabfall_by_product_line),
    template="plotly_white",
)
fig_product_Lebensmittelabfall.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    separators=",."
)

fig_product_Lebensmittelabfall.update_traces(
    
    selector=dict(type='bar'),
    texttemplate='%{value:.0f}',
    textposition='outside'
)

# Lebensmittelabfall BY Symptom [BAR CHART]
produktgruppe_chart = (
    df_selection.groupby(by=["Produktgruppe"]).sum()[["Menge"]].sort_values(by="Menge")
)
fig_produktgruppe_chart = px.bar(
    produktgruppe_chart,
    x="Menge",
    y=produktgruppe_chart.index,
    orientation="h",
   
    color_discrete_sequence=["#0083B8"] * len(Lebensmittelabfall_by_product_line),
    template="plotly_white",
)
fig_produktgruppe_chart.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    separators=",.",
    
)

fig_produktgruppe_chart.update_traces(
    legendrank=3,
    selector=dict(type='bar'),
    texttemplate='%{value:.0f}',
    textposition='outside',
)
##### Treemap ####

#navigation_name=["BU","Symptom"]
#navigation=st.radio("Navigation", navigation_name)





# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ---- MAINPAGE ----

st.title(":bar_chart: Lebensmittelabfall Dashboard")
st.markdown("##")

st.subheader(f"Menge Lebensmittelabfall: {Menge_Lebensmittelabfall} kg")
st.markdown("""---""")  
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Aufteilung BUs")
    st.plotly_chart(bu_grund)
with right_column:
    st.subheader("zeitlicher Verlauf")
    st.plotly_chart(verlauf)


st.markdown("""---""")

st.subheader("Gesamtüberblick: Abteilung - Produktgruppe - Symptom - Produktname - Datum")
st.plotly_chart(treemap)


st.markdown("""---""")

st.title("KPIs")

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Gesamtlebensmittelabfallquote in %") 
    st.plotly_chart(gesamtlebensmittelabfall)
with right_column:
    st.subheader("Maschinenabfallquote in %")
    st.plotly_chart(maschinenabfall)
st.markdown("""---""")

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Produktgruppen")
    st.plotly_chart(fig_produktgruppe_chart)
with right_column:
    st.subheader("Produktgruppen und Produktnamen")    
    st.plotly_chart(produkte)

st.markdown("""---""")



with left_column:
    st.subheader("Symptome")
    st.plotly_chart(fig_product_Lebensmittelabfall)
with right_column:
    st.subheader("Symptome und Gründe")    
    st.plotly_chart(gesamt_grund)



st.markdown("""---""")
st.title("Rohdaten")
raw_data = df_selection.replace({'nein': ""})
raw_data





