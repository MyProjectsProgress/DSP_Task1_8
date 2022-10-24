# ------------------------------------------------------------------------------------Importing liberaries
from matplotlib.lines import lineStyles
import streamlit as st
from numpy import sin,pi,linspace,zeros,arange,mean,sqrt,random,resize,sum,sinc,ceil,meshgrid,hypot
import matplotlib.pyplot as plt
import pandas as pd

col1,col2,col3 = st.columns([1,4,1])
# ------------------------------------------------------------------------------------General Plotting Signal
def general_signal_plotting(x_axis,y_axis):
    fig, axs = plt.subplots()
    fig.set_size_inches(11, 3)
    axs.plot(x_axis, y_axis)
    font1 = {'family':'serif','color':'white','size':20}
    plt.xlabel("Time (seconds)",fontdict = font1)
    plt.ylabel("Amplitude",fontdict = font1)
    plt.title("Composed Signal",fontdict = font1)
    st.plotly_chart(fig,use_container_width=True)
# ------------------------------------------------------------------------------------Setting Global Variables
list_of_objects = []
initial_time = linspace(0,2, 1000)
total_signals = sin(2*pi*initial_time)

# ------------------------------------------------------------------------------------Signal Object
class Signal:
    def __init__(self,amplitude,frequency):
        self.amplitude = amplitude 
        self.frequency = frequency
# ------------------------------------------------------------------------------------Adding Signals
def add_signal():
    col1,col2 = st.sidebar.columns(2)
    col11,col22,col33 = st.sidebar.columns([4,1,1])
    with col1:
        frequency = st.slider('Frequency (Hz)', min_value=1, max_value=50, step=1, key='frequency Box 22234') 
    with col2:
        amplitude = st.slider('Amplitude (m)', min_value=1, max_value=50, step=1, key='Amplitude Box 224') 

    with col22:
        add_button = st.button('Add', key="Save Button 22") 
    if add_button:
        adding_signals(frequency,amplitude) 
    
    signals_menu = []
    splitting_menu_contents = [] 
    for object in list_of_objects: 
        signals_menu.append(f'Frequency {object.frequency} Amplitude {object.amplitude}')
    with col11:
        signals_names = st.selectbox('Your Signals',signals_menu,key="lwflef") 

    splitting_menu_contents = str(signals_names).split(' ') 
    if len(splitting_menu_contents)==4: 
        removed_signal_freq = float(splitting_menu_contents[1]) 
        removed_signal_amp = float(splitting_menu_contents[3])
    with col33:
        remove_button = st.button('Del', key="Remove Button 22")
    if remove_button and len(list_of_objects)>0: 
        removing_signal(removed_signal_freq,removed_signal_amp) 
        st.experimental_rerun()

    # general_signal_plotting(initial_time,total_signals)
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

    contain = st.container()
    O,I,N,S = st.columns(4)
    with O:
        Original_Graph = st.checkbox('Original Graph',value=True,key='Original_Graph 123')
    with I:
        interpolation_check_box = st.checkbox('Interpolation',key='interpolation_check_box 132')
    with N:
        noise = st.checkbox('Noise' ,key="Noise Check Box 3432")
    with S:
        sampling = st.checkbox('Sampling Points' ,key="sampling Check Box 4232")

    sampling_method = st.sidebar.selectbox("The way of sampling",["Using F.maximum","Using sampling frequency"])
    if sampling_method == "Using F.maximum":
        max_freq = st.sidebar.slider(label= "F.maximum (Hz)",min_value=1,max_value=100,value=1,step=1)
        sampling_frequency = 2 * max_freq
    elif sampling_method == "Using sampling frequency":
        sampling_frequency = st.sidebar.slider(label='Sampling Frequency (Hz)', min_value=1, max_value=100, value=1, step=1)

    sample_rate = int((1000/2)/(sampling_frequency))
    time_axis = linspace(0, 2, 1000)
    sampled_time_axis= time_axis[::sample_rate]
    
    time_matrix = resize(time_axis, (len(sampled_time_axis), len(time_axis)))
    K = (time_matrix.T - sampled_time_axis) / (sampled_time_axis[1] - sampled_time_axis[0])

    if noise:
        #------------------- adding and sampling noise 
        noise_signal=add_noise()
        sampled_signals = noise_signal[::sample_rate]
        total_signals=noise_signal
        #------------------Reconstructed  signals of noise
        final_matrix = sampled_signals * sinc(K)
    else:
        #----------------- sampling signals without noise
        sampled_signals= total_signals[::sample_rate]
        #------------------------------ Reconstruct noise signal with noise -------------------------------#
        final_matrix = sampled_signals * sinc(K)

    reconstructed_signal = sum(final_matrix, axis=1)

    fig, axs = plt.subplots()
    fig.set_size_inches(11, 3.5)

    if interpolation_check_box:
        axs.plot(time_axis,reconstructed_signal,color='Red',linestyle='dashed',alpha=1)

    if Original_Graph:
        axs.plot(time_axis,total_signals, color='royalblue')

    if sampling:
        axs.plot(sampled_time_axis, sampled_signals, color='green' , marker="o" ,linestyle="" ,alpha=0.7)

    x_zero_line = linspace(0,2,1000)
    y_zero_line = zeros(1000)
    axs.plot(x_zero_line , y_zero_line, color='grey', alpha = 0.5)

    plt.xlim(0,2)
    font1 = {'family':'serif','color':'white','size':20}
    plt.xlabel("Time (seconds)",fontdict = font1)
    plt.ylabel("Amplitude",fontdict = font1)
    plt.title("Reconstructed Signal",fontdict = font1)
    contain.plotly_chart(fig,use_container_width=True)
# ------------------------------------------------------------------------------------Adding Noise
def add_noise():

    SNR = st.sidebar.slider(label='SNR', min_value=1, max_value=50, value=25, step=1)
    signal_power = total_signals **2                                    # Generating the signal power
    signal_power_avg = mean(signal_power)                               # mean of signal power
    noise_power = signal_power_avg / SNR
    mean_noise = 0
    noise = random.normal(mean_noise,sqrt(noise_power),len(total_signals))
    noise_signal = total_signals + noise
    return noise_signal