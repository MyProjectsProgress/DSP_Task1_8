import streamlit as st
from random import randint
import pandas as pd
import uploaded_signals_fn as USF
import generated_signal_fn as GSF

# ------------------------------------------------------------------------------------Front end 
with open("design.css") as source_ds:
    st.markdown(f"<style>{source_ds.read()}</style>",unsafe_allow_html=True)
col11,col22,col33 = st.columns([1,1,1])
dataset = st.sidebar.file_uploader("Sampling Studio", type = ['csv'])
# ------------------------------------------------------------------------------------ User Options
options = st.sidebar.radio('Tools', options=['Uploaded Signal Studio','Signal Generation Studio'])

# ------------------------------------------------------------------------------------Uploaded Signal Studio
def uploaded_signal_studio():
    if dataset is not None:
        df = pd.read_csv(dataset)
        df_x_axis,df_y_axis = USF.get_data_frame(df)
        add_noise_button = st.checkbox("Add Noise")
        if add_noise_button:
            USF.add_noise(df)
        else:
            USF.general_signal_plotting(df_x_axis,df_y_axis)
        USF.add_signal(df)
        sampled_amplitude, sampled_time = USF.signal_sampling(df)
        time_points, reconstructed_signal = USF.signal_reconstructing(df, sampled_time, sampled_amplitude)
        USF.sampling_signal_plotting(df,sampled_time,sampled_amplitude)
        USF.general_signal_plotting(time_points, reconstructed_signal)
        st.download_button('Download Your Data', df.to_csv(),file_name= f'Data With Code #{randint(0, 1000)}.csv' ,mime = 'text/csv',key="Download Button")

# ------------------------------------------------------------------------------------Generated Signal Studio
def generated_signal_studio():
    GSF.sin_signal_viewer()
    GSF.add_signal()
    GSF.Sampling()

# ------------------------------------------------------------------------------------Radio Buttons
if options == 'Uploaded Signal Studio':
    uploaded_signal_studio()
elif options == 'Signal Generation Studio':
    generated_signal_studio()