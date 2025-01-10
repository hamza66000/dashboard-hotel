import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(page_title="Superstore EDA", page_icon=":bar_chart:", layout="wide")

# Page title and styling
st.title(":bar_chart: Sample SuperStore EDA")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

# File uploader
fl = st.file_uploader(':file_folder: Upload a File', type=["csv", "txt", "xlsx", "xls"])

if fl is not None:
    # If a file is uploaded, determine its type and load it
    filename = fl.name
    st.write(f"File Uploaded: {filename}")

    if filename.endswith(('.csv', '.txt')):
        # Load CSV or TXT files
        df = pd.read_csv(fl, encoding="ISO-8859-1")
    elif filename.endswith(('.xlsx', '.xls')):
        # Load Excel files
        df = pd.read_excel(fl)

    # Display the dataset
    st.write("Dataset Preview:")
    st.dataframe(df)

    # Basic Dataset Information
    st.write("Dataset Info:")
    st.write(df.describe())
    st.write(df.info())

else:
    # If no file is uploaded, display instructions
    st.write("Please upload a CSV or Excel file to proceed.")

col1,col2 = st.columns((2))
df["order date"] = pd.to_datetime(df["order date"]) 

#getting the min and max date
startdate = pd.to_datetime(df["order date"]).min()
enddate = pd.to_datetime(["order date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("start date", enddate))

df = df[(df["order date"] >= date1) & (df["order date"] <= date2)].copy()
