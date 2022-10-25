import streamlit as st
st.set_page_config(layout="wide")
from random import randint
import pandas as pd
import uploaded_signals_fn as USF
import generated_signal_fn as GSF
import numpy as np

# ------------------------------------------------------------------------------------ User Options
dataset = st.file_uploader(label="Uploading Signal", type = ['csv'])

# ------------------------------------------------------------------------------------Uploaded and Genertaed Signal Studios
def generated_signal_studio():
    total_signals=GSF.add_signal()
    reconstructed_signal = GSF.Sampling_added_signals(total_signals)
    time = np.linspace(0,2,1000)
    df = pd.DataFrame({'Time (sc)': time, 'Amplitudes (m)': reconstructed_signal}, columns=['Time (sc)','Amplitudes (m)'])
    st.sidebar.download_button('Download Your Data', df.to_csv(index=False),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 1999")

if dataset is not None:
    df = pd.read_csv(dataset)
    total_signals = USF.add_signal(df)
    reconstructed_signal,end_time,begin_time = USF.signal_sampling(df,total_signals)
    time = np.linspace(begin_time,end_time,len(reconstructed_signal))
    df = pd.DataFrame({'Time (sc)': time, 'Amplitudes (m)': reconstructed_signal}, columns=['Time (sc)','Amplitudes (m)'])
    st.sidebar.download_button('Download Your Data', df.to_csv(index=False),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 2022")
else:
    generated_signal_studio()