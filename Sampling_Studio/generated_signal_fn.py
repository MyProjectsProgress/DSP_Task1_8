# ------------------------------------------------------------------------------------Importing Liberaries
import streamlit as st
from numpy import sin,pi,linspace,zeros,arange,mean,sqrt,random,resize,sum,sinc,ceil
import matplotlib.pyplot as plt
import pandas as pd
from random import randint
from scipy import interpolate
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline

# ------------------------------------------------------------------------------------Sin Signal Viewer Function For Home Function
# def sin_signal_viewer():
#     time = linspace(-1, 1, 1000)
#     frequency = st.slider(label='Frequency', min_value=1, max_value=150, step=1)
#     amplitude = st.slider(label='Amplitude', min_value=1, max_value=150, step=1)
#     sin_signal = amplitude*sin(2*pi*frequency *time) 

#     fig, axs = plt.subplots()
#     fig.set_size_inches(11, 4)
#     axs.plot(time, sin_signal)
#     st.plotly_chart(fig)

# ------------------------------------------------------------------------------------General Plotting Signal
def general_signal_plotting(x_axis,y_axis):
    fig, axs = plt.subplots()
    fig.set_size_inches(11, 4)
    axs.plot(x_axis, y_axis)
    st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------------------------------------------Setting Global Variables
list_of_objects = []
initial_time = linspace(-1,1, 1000)
total_signals = zeros(1000)

# ------------------------------------------------------------------------------------Signal Object
class Signal:
    def __init__(self,amplitude,frequency):
        self.amplitude = amplitude 
        self.frequency = frequency

# ------------------------------------------------------------------------------------Adding Signals
def main_add_signal():
    col1,col2 = st.columns([1,2])
    with col1:
        frequency = col1.slider('Choose Frequency', min_value=1, max_value=50, step=1, key='frequency Box') 
        amplitude = col1.slider('Choose Amplitude', min_value=1, max_value=50, step=1, key='Amplitude Box') 

        add_button = col1.button('Add Signal', key="Save Button") 
        if add_button:
            summing_signals(frequency,amplitude) 
        
        signals_menu = []
        splitting_menu_contents = [] 
        for object in list_of_objects: 
            signals_menu.append(f'Frequency {object.frequency} Amplitude {object.amplitude}')
        
        signals_names = col1.selectbox('Your Signals',signals_menu) 

        splitting_menu_contents = str(signals_names).split(' ') 
        if len(splitting_menu_contents)==4: 
            removed_signal_freq = float(splitting_menu_contents[1]) 
            removed_signal_amp = float(splitting_menu_contents[3])

        remove_button = col1.button('Remove Signal', key="Remove Button")
        if remove_button and len(list_of_objects)>0: 
            removing_signals(removed_signal_freq,removed_signal_amp) 
    with col2:
        general_signal_plotting(initial_time,total_signals)
# ------------------------------------------------------------------------------------Adding Signals
def summing_signals(frequency,amplitude):                                              
    global total_signals                                                              
    total_signals = zeros(1000)                                                       
    list_of_objects.append(Signal(frequency=frequency, amplitude=amplitude))          
    for object in list_of_objects:                                                    
        object_frequency = object.frequency                                           
        object_amplitude = object.amplitude                                           
        signal_y_axis = object_amplitude*sin(2*pi*object_frequency*initial_time)      
        total_signals += signal_y_axis

# ------------------------------------------------------------------------------------Removing Added Signals
def removing_signals(removed_freq,removed_amp):
    global total_signals 
    total_signals = zeros(1000)

    for object in list_of_objects:
        if removed_freq == object.frequency and removed_amp == object.amplitude:
            list_of_objects.remove(object)
            break

    for object in list_of_objects:
        object_frequency = object.frequency
        object_amplitude = object.amplitude
        signal_y_axis = object_amplitude*sin(2*pi*object_frequency*initial_time)
        total_signals += signal_y_axis

# ------------------------------------------------------------------------------------Sampling Signals
def sampling():

    amplitude          = st.slider(label='Amplitude', min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    signal_frequency   = st.slider(label='Frequency', min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    sampling_frequency = st.slider(label='Sampling', min_value=1.0, max_value=150.0, value=float(ceil(2*signal_frequency)), step=1.0)

    sampling_period=1/sampling_frequency                                    #Ts

    col1,col2 = st.columns([1,1])
    
    showing_signal          = col1.checkbox('Show Orginal Signal on Graph')
    interpolation_check_box = col2.checkbox('Interpolation')

    sampled_time_axis      = arange(0, 8, sampling_period)                  #time steps

    sampled_amplitude_axis = amplitude * sin(2*pi*signal_frequency*sampled_time_axis) 

    time_axis      = linspace(0, 8, 1000)
    amplitude_axis = amplitude*sin(2*pi*signal_frequency * time_axis )

    fig2, axs = plt.subplots()
    fig2.set_size_inches(6, 4)

    if showing_signal:
        axs.plot(time_axis, amplitude_axis, color='red', linewidth=3, linestyle='-')
    elif interpolation_check_box :
        time_matrix = resize(time_axis, (len(sampled_time_axis), len(time_axis)))
        K = (time_matrix.T - sampled_time_axis) / (sampled_time_axis[1] - sampled_time_axis[0])
        final_matrix = sampled_amplitude_axis * sinc(K)
        reconstructed_signal = sum(final_matrix, axis=1)
        axs.plot(time_axis,reconstructed_signal,color='green',linestyle='-')
    axs.plot(sampled_time_axis, sampled_amplitude_axis,color="blue",linestyle='', marker='o' ,markersize=3 )
    axs.axhline(0, color='black', linestyle='-', linewidth=0)
    col1.plotly_chart(fig2,use_container_width=True)
    fig, axs = plt.subplots()
    fig.set_size_inches(6, 4)
    axs.plot(time_axis, amplitude_axis)
    col2.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------------------------------------------Removing Added Signals
def add_noise():

    SNR = st.slider(label='SNR', min_value=0.0, max_value=50.0, value=1.0, step=1.0)

    signal_power = total_signals **2      # Generating the signal power
    
    signal_power_avg = mean(signal_power) # mean of signal power

    if (SNR==0):
        noise_power = signal_power_avg / 0.00001
    else:
        noise_power = signal_power_avg / SNR
    mean_noise = 0
    noise = random.normal(mean_noise,sqrt(noise_power),len(total_signals))
    noise_signal = total_signals + noise

    return noise_signal
