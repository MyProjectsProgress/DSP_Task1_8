# ------------------------------------------------------------------------------------
""" 
This file includes callling functions from other files
"""

# ------------------------------------------------------------------------------------Importing Files and Libraries
import streamlit as st
from random import randint
import pandas as pd
import uploaded_signals_fn as USF
import generated_signal_fn as GSF
import numpy as np

# ------------------------------------------------------------------------------------Front end 
st.set_page_config(layout="wide")
with open("design.css") as source_ds:
    st.markdown(f"<style>{source_ds.read()}</style>",unsafe_allow_html=True)

# ------------------------------------------------------------------------------------ User Options
options = st.sidebar.radio('Site Tabs', options=['Uploaded Signal Studio','Signal Generation Studio'])
tab1, tab2 = st.tabs(['Show File Browse', 'Hide File Browse'])
with tab1:
    dataset = st.file_uploader("Upload Your File Here", type = ['csv'])

# ------------------------------------------------------------------------------------Uploaded Signal Studio
def uploaded_signal_studio():
    if dataset is not None:
        df = pd.read_csv(dataset)
        df_x_axis,df_y_axis = USF.get_data_frame(df)
        USF.add_signal(df)
        sampled_amplitude, sampled_time ,df_y_axis = USF.signal_sampling(df)
        time_points, reconstructed_signal = USF.signal_reconstructing(df, sampled_time, sampled_amplitude)
        USF.sampling_signal_plotting(df,df_y_axis,sampled_time,sampled_amplitude)
        USF.general_signal_plotting(time_points, reconstructed_signal)
        st.sidebar.download_button('Download Your Data', df.to_csv(),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 42332")
    else:
        st.header("Upload Your Signal to Start Applying Functions")
        GSF.sin_signal_viewer()
# ------------------------------------------------------------------------------------Generated Signal Studio
def generated_signal_studio():
    total_signals=GSF.add_signal()
    GSF.Sampling_added_signals(total_signals)
    time = np.linspace(-1,1,1000)
    df = pd.DataFrame({'Time (sc)': time, 'Amplitudes (m)': total_signals}, columns=['Time (sc)','Amplitudes (m)'])
    st.sidebar.download_button('Download Your Data', df.to_csv(index=False),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button 11276")

# ------------------------------------------------------------------------------------Radio Buttons
if options == 'Uploaded Signal Studio':
    uploaded_signal_studio()
elif options == 'Signal Generation Studio':
    generated_signal_studio()
