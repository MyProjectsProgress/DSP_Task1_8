from typing import Container
import streamlit as st
st.set_page_config(layout="wide")
from random import randint
import pandas as pd
import uploaded_signals_fn as USF
import generated_signal_fn as GSF
import numpy as np

# ------------------------------------------------------------------------------------Front end 
with open("design.css") as source_ds:
    st.markdown(f"<style>{source_ds.read()}</style>",unsafe_allow_html=True)

# ------------------------------------------------------------------------------------ User Options
dataset = st.sidebar.file_uploader(label="", type = ['csv'])

# ------------------------------------------------------------------------------------Calling Main Functions
if dataset is not None:
    df = pd.read_csv(dataset)
    total_signals = USF.add_signal(df)
    reconstructed_signal,end_time,begin_time = USF.signal_sampling(df,total_signals)
    time = np.linspace(begin_time,end_time,len(reconstructed_signal))
    df = pd.DataFrame({'Time (Sc)': time, 'Amplitudes (V)': reconstructed_signal}, columns=['Time (Sc)','Amplitudes (V)'])
    st.sidebar.download_button('Download Your Data', df.to_csv(index=False),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 2022")
else:
    total_signals=GSF.add_signal()
    reconstructed_signal = GSF.signal_sampling(total_signals)
    time = np.linspace(0,2,1000)
    df = pd.DataFrame({'Time (Sc)': time, 'Amplitudes (V)': reconstructed_signal}, columns=['Time (Sc)','Amplitudes (V)'])
    st.sidebar.download_button('Download Your Data', df.to_csv(index=False),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 1999")