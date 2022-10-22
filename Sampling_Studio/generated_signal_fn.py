# ------------------------------------------------------------------------------------Importing liberaries
from turtle import width
from matplotlib.lines import lineStyles
import streamlit as st
from numpy import sin,pi,linspace,zeros,arange,mean,sqrt,random,resize,sum,sinc,ceil
import matplotlib.pyplot as plt
import pandas as pd
from random import randint
from scipy import interpolate
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline

# ------------------------------------------------------------------------------------Sin Plotting Signal
def sin_signal_viewer():
    time = linspace(-1, 1, 1000)
    frequency = st.sidebar.slider(label='Frequency (Hz)', min_value=1, max_value=50, step=1)
    amplitude = st.sidebar.slider(label='Amplitude (m)', min_value=1, max_value=50, step=1)
    sin_signal = amplitude*sin(2*pi*frequency*time) 

    fig, axs = plt.subplots()
    fig.set_size_inches(11, 3)
    font1 = {'family':'serif','color':'white','size':20}
    plt.xlabel("Time",fontdict = font1)
    plt.ylabel("Amplitude",fontdict = font1)
    axs.plot(time, sin_signal)
    st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------------------------------------------General Plotting Signal
def general_signal_plotting(x_axis,y_axis):
    fig, axs = plt.subplots()
    fig.set_size_inches(11, 3)
    axs.plot(x_axis, y_axis)
    font1 = {'family':'serif','color':'white','size':20}
    plt.xlabel("Time",fontdict = font1)
    plt.ylabel("Amplitude",fontdict = font1)
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
def add_signal():
    col11,col22 = st.columns([1,1])
    col1,col2,col3 = st.columns([1,1,1])

    frequency = col11.slider('Frequency (Hz)', min_value=1, max_value=50, step=1, key='frequency Box 22234') 
    amplitude = col22.slider('Amplitude (m)', min_value=1, max_value=50, step=1, key='Amplitude Box 224') 

    add_button = col1.button('Add Signal', key="Save Button 22") 
    if add_button:
        adding_signals(frequency,amplitude) 
    
    signals_menu = []
    splitting_menu_contents = [] 
    for object in list_of_objects: 
        signals_menu.append(f'Frequency {object.frequency} Amplitude {object.amplitude}')
    
    signals_names = st.sidebar.selectbox('Your Signals',signals_menu,key="lwflef") 

    splitting_menu_contents = str(signals_names).split(' ') 
    if len(splitting_menu_contents)==4: 
        removed_signal_freq = float(splitting_menu_contents[1]) 
        removed_signal_amp = float(splitting_menu_contents[3])

    remove_button = col3.button('Remove Signal', key="Remove Button 22")
    if remove_button and len(list_of_objects)>0: 
        removing_signal(removed_signal_freq,removed_signal_amp) 

    general_signal_plotting(initial_time,total_signals)

    return total_signals
# ------------------------------------------------------------------------------------Adding Signals
def adding_signals(frequency,amplitude):                                              
    global total_signals                                                              
    total_signals = zeros(1000)                                                       
    list_of_objects.append(Signal(frequency=frequency, amplitude=amplitude))          
    for object in list_of_objects:                                                    
        object_frequency = object.frequency                                           
        object_amplitude = object.amplitude                                           
        signal_y_axis = object_amplitude*sin(2*pi*object_frequency*initial_time)      
        total_signals += signal_y_axis

# ------------------------------------------------------------------------------------Removing Added Signals
def removing_signal(removed_freq,removed_amp):
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

# ------------------------------------------------------------------------------------Sampling Added Signals
def Sampling_added_signals(total_signals):

    sampling_frequency = st.sidebar.slider(label='Sampling Frequency (Hz)', min_value=1, max_value=100, value=1, step=1)
    sampling_period=1/sampling_frequency

    sample_rate = int((1000/2)/(sampling_frequency))
    if sample_rate == 0:
        sample_rate = 1
    
    time_axis      = linspace(-1, 1, 1000)                 
    sampled_time_axis      = time_axis[::sample_rate]  

    fig, axs = plt.subplots()
    fig.set_size_inches(11, 3)

    noise_signal=add_noise()
    noise_sampled_y_axis = noise_signal[::sample_rate]

    Original_Graph = st.sidebar.checkbox('Original Graph',key='Original_Graph 123')
    interpolation_check_box = st.sidebar.checkbox('Interpolation',key='interpolation_check_box 132')
    noise = st.sidebar.checkbox('Noise', key="Noise Check Box 3432")

    if noise and interpolation_check_box and Original_Graph :

        time_matrix = resize(time_axis, (len(sampled_time_axis), len(time_axis)))
        K = (time_matrix.T - sampled_time_axis) / (sampled_time_axis[1] - sampled_time_axis[0])
        final_matrix = noise_sampled_y_axis * sinc(K)
        reconstructed_signal = sum(final_matrix, axis=1)

        axs.plot(sampled_time_axis, noise_sampled_y_axis ,color='yellow' ,marker="o" ,linestyle='',alpha=0.7)
        axs.plot(time_axis,reconstructed_signal,color='Red',linestyle='dashed',alpha=0.7)
        axs.plot(time_axis,noise_signal, color='royalblue', alpha=0.4)
    
    elif noise and interpolation_check_box :

        time_matrix = resize(time_axis, (len(sampled_time_axis), len(time_axis)))
        K = (time_matrix.T - sampled_time_axis) / (sampled_time_axis[1] - sampled_time_axis[0])
        final_matrix = noise_sampled_y_axis * sinc(K)
        reconstructed_signal = sum(final_matrix, axis=1)

        axs.plot(sampled_time_axis, noise_sampled_y_axis ,color='yellow' ,marker="o" ,linestyle='',alpha=0.7)
        axs.plot(time_axis,reconstructed_signal,color='Red',linestyle='dashed',alpha=0.7)
    
    elif noise and Original_Graph :

        total_signals_sampled= total_signals[::sample_rate]
        axs.plot(sampled_time_axis, total_signals_sampled ,color='yellow' ,marker="o" ,linestyle='',alpha=0.7)
        axs.plot(time_axis,noise_signal, color='royalblue' ,linewidth=1,  alpha=0.4)

    elif interpolation_check_box and Original_Graph :

        total_signals_sampled= total_signals[::sample_rate]
        time_matrix = resize(time_axis, (len(sampled_time_axis), len(time_axis)))
        K = (time_matrix.T - sampled_time_axis) / (sampled_time_axis[1] - sampled_time_axis[0])
        final_matrix = total_signals_sampled * sinc(K)
        reconstructed_signal = sum(final_matrix, axis=1)

        axs.plot(time_axis,reconstructed_signal,color='Red',linestyle='dashed',alpha=0.9)
        axs.plot(sampled_time_axis, total_signals_sampled , marker="o" ,linestyle="")
        axs.plot(time_axis,total_signals, color='royalblue',alpha=0.4)

    elif noise:
        axs.plot(sampled_time_axis, noise_sampled_y_axis ,color='yellow' ,marker="o" ,linestyle='')
        # axs.plot(time_axis,noise_signal, color='royalblue' ,linewidth=1,  alpha=0.4)

    elif interpolation_check_box:

        total_signals_sampled= total_signals[::sample_rate]
        time_matrix = resize(time_axis, (len(sampled_time_axis), len(time_axis)))
        K = (time_matrix.T - sampled_time_axis) / (sampled_time_axis[1] - sampled_time_axis[0])
        final_matrix = total_signals_sampled * sinc(K)
        reconstructed_signal = sum(final_matrix, axis=1)

        axs.plot(time_axis,reconstructed_signal,color='Red',linestyle='dashed',alpha=0.7)
        axs.plot(sampled_time_axis, total_signals_sampled ,color='yellow' ,marker="o" ,linestyle='',alpha=0.7)

    elif Original_Graph:

        total_signals_sampled= total_signals[::sample_rate]
        axs.plot(sampled_time_axis, total_signals_sampled ,color='yellow' ,marker="o" ,linestyle='',alpha=0.7)
        axs.plot(time_axis,total_signals, color='royalblue')

    else:
        total_signals_sampled= total_signals[::sample_rate]
        axs.plot(sampled_time_axis, total_signals_sampled , marker="o" ,linestyle="")

    font1 = {'family':'serif','color':'white','size':20}
    plt.xlabel("Time",fontdict = font1)
    plt.ylabel("Amplitude",fontdict = font1)
    st.plotly_chart(fig,use_container_width=True)
# ------------------------------------------------------------------------------------Removing Added Signals
def add_noise():

    SNR = st.sidebar.slider(label='SNR', min_value=0.0, max_value=50.0, value=0.0, step=0.1)

    signal_power = total_signals **2                                    # Generating the signal power
    
    signal_power_avg = mean(signal_power)                               # mean of signal power

    if (SNR==0):
        noise_power = signal_power_avg / 0.0000001
    else:
        noise_power = signal_power_avg / SNR
    mean_noise = 0
    noise = random.normal(mean_noise,sqrt(noise_power),len(total_signals))
    noise_signal = total_signals + noise

    return noise_signal