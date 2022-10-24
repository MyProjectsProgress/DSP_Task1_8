import streamlit as st
st.set_page_config(layout="wide")
from random import randint
import pandas as pd
import uploaded_signals_fn as USF
import generated_signal_fn as GSF
import numpy as np

# ------------------------------------------------------------------------------------Front end 

# container = st.sidebar.container()

# with open("design.css") as source_ds:
#     st.markdown(f"<style>{source_ds.read()}</style>",unsafe_allow_html=True)

# ------------------------------------------------------------------------------------ User Options
dataset = st.file_uploader(label="Uploading Signal", type = ['csv'])

# ------------------------------------------------------------------------------------Uploaded Signal Studio
def generated_signal_studio():
    total_signals=GSF.add_signal()
    GSF.Sampling_added_signals(total_signals)

if dataset is not None:
    df = pd.read_csv(dataset)
    total_signals = USF.add_signal(df)
    USF.signal_sampling(df,total_signals)
    # st.sidebar.download_button('Download Your Data', df.to_csv(),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 42332")
else:
    generated_signal_studio()

# ------------------------------------------------------------------------------------Generated Signal Studio

    # time = np.linspace(0,2,1000)
    # df = pd.DataFrame({'Time (sc)': time, 'Amplitudes (m)': total_signals}, columns=['Time (sc)','Amplitudes (m)'])
    # st.sidebar.download_button('Download Your Data', df.to_csv(index=False),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 11276")