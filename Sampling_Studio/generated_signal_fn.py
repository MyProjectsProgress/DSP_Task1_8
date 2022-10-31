# ------------------------------------------------------------------------------------Importing liberaries
from matplotlib.lines import lineStyles
import streamlit as st
from numpy import sin,pi,linspace,zeros,arange,mean,sqrt,random,resize,sum,sinc,ceil,meshgrid,hypot
import matplotlib.pyplot as plt
import pandas as pd
import scipy.fft
from scipy.signal import find_peaks
import numpy as np
col1,col2,col3 = st.columns([1,4,1])   #Dividing front end page into 3 columns 
# ------------------------------------------------------------------------------------Setting Global Variables
list_of_objects = []                   #Contains objects created from Signal class
initial_time = linspace(0,2, 1000)     #x_axis of any sin wave signal 
total_signals = zeros(1000)            #initial value of the y_axis of the generated signals

# ------------------------------------------------------------------------------------Signal class that contains the frequency and amplitude of each signal
class Signal:
    def __init__(self,amplitude,frequency):
        self.amplitude = amplitude 
        self.frequency = frequency

# ------------------------------------------------------------------------------------Adding Signals: Contains the sliders that creates sin waves then calling the function that add them and remove them and return the total signals
def add_signal():
    col1,col2 = st.sidebar.columns(2)
    col11,col22,col33 = st.sidebar.columns([4,1,1])
    with col1:
        frequency = st.slider('Frequency (Hz)', min_value=1, max_value=50, step=1, key='frequency Box 123') 
    with col2:
        amplitude = st.slider('Amplitude (Volt)', min_value=1, max_value=50, step=1, key='Amplitude Box 122') 

    with col22:
        add_button = st.button('Add', key="Save Button 22") 
    if add_button:
        summing_signals(frequency,amplitude) 
    
    signals_menu = []
    splitting_menu_contents = [] 
    for object in list_of_objects: 
        signals_menu.append(f'Freq: {object.frequency} Amp: {object.amplitude}')
    with col11:
        signals_names = st.selectbox('Your Signals',signals_menu,key="Your Signal") 

    splitting_menu_contents = str(signals_names).split(' ') 
    if len(splitting_menu_contents)==4: 
        removed_signal_freq = float(splitting_menu_contents[1]) 
        removed_signal_amp = float(splitting_menu_contents[3])
    with col33:
        remove_button = st.button('Delete', key="Remove Button 22")
    if remove_button and len(list_of_objects)>0: 
        removing_signal(removed_signal_freq,removed_signal_amp) 
        st.experimental_rerun()

    return total_signals

# ------------------------------------------------------------------------------------Summing sin waves amplitudes and returning the total signal after this summation
def summing_signals(frequency,amplitude):
    global total_signals                                                              
    total_signals = zeros(1000)
    list_of_objects.append(Signal(frequency=frequency, amplitude=amplitude))
    for object in list_of_objects:
        object_frequency = object.frequency
        object_amplitude = object.amplitude
        signal_y_axis = object_amplitude*sin(2*pi*object_frequency*initial_time)      
        total_signals += signal_y_axis

# ------------------------------------------------------------------------------------Removing a signal then summing all signals and returning the total signal
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

# ------------------------------------------------------------------------------------Sampling total signals after adding noise or adding sin waves or even deleting one or more signal and returning the reconstructed signal to dowonload it
def signal_sampling(total_signals):
    contain = st.container()
    col1,col2 = st.sidebar.columns(2)
    column1,column2,column3,column4 = st.columns(4)
    with column1:
        Original_Graph          = col1.checkbox('Original Signal',value=True,key='Original_Graph 10')
    with column2:
        interpolation_check_box = col1.checkbox('Interpolation',key='interpolation_check_box 11')
    with column3:
        noise                   = col2.checkbox('Add Noise' ,key="Noise Check Box 12")
    with column4:
        sampling                = col2.checkbox('Sampling Points' ,key="sampling Check Box 13")
    
    amplitude = np.abs(scipy.fft.rfft(total_signals))
    frequency = scipy.fft.rfftfreq(len(initial_time), (initial_time[1]-initial_time[0]))
    indices = find_peaks(amplitude)

    if len(indices[0])>0 :
        max_freq=round(frequency[indices[0][-1]])
    else:
        max_freq=1   

    if sampling or interpolation_check_box  :
        sampling_options = st.sidebar.selectbox('Sampling Frequency Options' ,["Actual Sampling Frequency", f"Sampling Relative to Max Frequency: {max_freq} Hz"], key="Options")
        if sampling_options == "Actual Sampling Frequency":
            sampling_frequency = st.sidebar.slider(label= "",min_value=1,max_value=100,value=1,step=1)
        else:
            sampling_frequency = max_freq * st.sidebar.slider(label= "",min_value=1,max_value=10,value=2,step=1)
    else:
        sampling_frequency=1

    sample_step = int(((1000/2)/(sampling_frequency)))
    time_axis = linspace(0, 2, 1000)
    sampled_time_axis = time_axis[::sample_step]
    
    time_matrix = resize(time_axis, (len(sampled_time_axis), len(time_axis)))
    plotted_matrix = (time_matrix.T - sampled_time_axis) / (sampled_time_axis[1] - sampled_time_axis[0])

    if noise:
        #------------------------------ Adding and sampling noise ----------------------------------------#
        noise_signal=add_noise()
        sampled_signals = noise_signal[::sample_step]
        total_signals=noise_signal
    else:
        #------------------------------ Sampling signals without noise ------------------------------------#
        sampled_signals= total_signals[::sample_step]
        
    #------------------------------ Reconstruct noise signal with noise -------------------------------#
    final_matrix = sampled_signals * sinc(plotted_matrix)
    reconstructed_signal = sum(final_matrix, axis=1)

    fig, axs = plt.subplots()
    fig.set_size_inches(14,5)

    if interpolation_check_box:
        axs.plot(time_axis,reconstructed_signal,color='red',alpha=1,label="Reconstructed",linewidth=2)

    if Original_Graph:
        axs.plot(time_axis,total_signals, color='darkslategrey',alpha=0.5,label="Original")

    if sampling:
        axs.plot(sampled_time_axis, sampled_signals, color='black' , marker="o" ,linestyle="" ,alpha=0.8,label="Sampled",markersize=4)

    x_zero_line = linspace(0,2,1000)
    y_zero_line = zeros(1000)
    axs.plot(x_zero_line , y_zero_line, color='grey', alpha = 0.2)

    plt.xlim(0,2)
    font1 = {'family':'serif','color':'black','size':20}
    plt.xlabel("Time (Seconds)",fontdict = font1)
    plt.ylabel("Amplitude (Volt)",fontdict = font1)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5,0.5,0.7),fontsize = 11)
    contain.plotly_chart(fig,use_container_width=True)

    return reconstructed_signal

# ------------------------------------------------------------------------------------Adding Noise to signal then returning the noised signal
def add_noise():
    SNR = st.sidebar.slider(label='SNR', min_value=1, max_value=50, value=25, step=1)
    signal_power = total_signals **2                                    # Generating the signal power
    signal_power_avg = mean(signal_power)                               # mean of signal power
    noise_power = signal_power_avg / SNR
    mean_noise = 0
    noise = random.normal(mean_noise,sqrt(noise_power),len(total_signals))
    noise_signal = total_signals + noise
    return noise_signal