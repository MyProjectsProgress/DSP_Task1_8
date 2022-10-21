# ------------------------------------------------------------------------------------Importing liberaries
import streamlit as st
from numpy import sin,pi,linspace,zeros,arange,mean,sqrt,random,resize,sum,sinc
import matplotlib.pyplot as plt
import pandas as pd
from random import randint

# ------------------------------------------------------------------------------------Getters

def get_data_frame(df):
    
    list_of_columns = df.columns
    df_x_axis = df[list_of_columns[0]]
    df_y_axis = df[list_of_columns[1]]
    return df_x_axis,df_y_axis

# ------------------------------------------------------------------------------------Setting Global Variables
list_of_objects = []

# ------------------------------------------------------------------------------------Signal Object
class Signal:
    def __init__(self,amplitude,frequency):
        self.amplitude = amplitude 
        self.frequency = frequency

# ------------------------------------------------------------------------------------General Plotting Signal
def general_signal_plotting(x_axis,y_axis):

    fig, axs = plt.subplots()
    fig.set_size_inches(11, 4)
    axs.plot(x_axis, y_axis)
    st.plotly_chart(fig)

# ------------------------------------------------------------------------------------General Plotting Signal
def sampling_signal_plotting(df,df_y_axis,x_sampled_axis,y_sampled_axis):

    list_of_columns = df.columns
    # df_y_axis = df[list_of_columns[1]]
    df_x_axis = df[list_of_columns[0]]

    fig, axs = plt.subplots()
    fig.set_size_inches(11, 4)
    axs.plot(df_x_axis, df_y_axis)
    axs.plot(x_sampled_axis, y_sampled_axis,marker='o',linestyle='')
    st.plotly_chart(fig)

# ------------------------------------------------------------------------------------Adding & Removing Signal Function 
def add_signal(df):
    global total_signals
    col1,col2 = st.columns([1,2])

    list_of_columns = df.columns
    df_y_axis = df[list_of_columns[1]]
    corresponding_x_axis = linspace(-1,1, len(df_y_axis))

    if len(list_of_objects)==0: 
        total_signals = df_y_axis
    else:
        total_signals = df_y_axis
        for object in list_of_objects:
            object_frequency = object.frequency
            object_amplitude = object.amplitude
            signal_y_axis = object_amplitude*sin(2*pi*object_frequency*corresponding_x_axis)
            total_signals += signal_y_axis

    frequency = col1.slider('Choose Frequency', min_value=1, max_value=50, step=1, key='frequency Box') 
    amplitude = col1.slider('Choose Amplitude', min_value=1, max_value=50, step=1, key='Amplitude Box') 

    add_button = col1.button('Add Signal', key="Save Button") 
    if add_button:
        total_signals = adding_sin_waves(frequency,amplitude,df_y_axis,corresponding_x_axis)

    signals_menu = [] 
    splitting_menu_contents = [] # List that contains the signal name so that we split that name and get its amp and freq
    for object in list_of_objects: # Looping over the list ob objects to append a name of each object in the select box
        signals_menu.append(f'Frequency {object.frequency} Amplitude {object.amplitude}') # Appending a unique name to each signal based on its amp and freq values
    
    signals_names = col1.selectbox('Your Signals',signals_menu) # The select box which contains object names

    splitting_menu_contents = str(signals_names).split(' ') # Splitting the name into 4 values: ['Frequency', 'object.frequency', 'Amplitude',  'object.amplitude']
    if len(splitting_menu_contents)==4: # Checking if the list contains these 4 values or empty 
        removed_signal_freq = float(splitting_menu_contents[1]) # Pick the frequency value
        removed_signal_amp = float(splitting_menu_contents[3]) # Pick the frequency value

    remove_button = col1.button('Remove Signal', key="Remove Button") 

    if remove_button and len(list_of_objects)>0:
        total_signals = removing_signal(df,removed_signal_freq,removed_signal_amp) 

    fig, axs = plt.subplots()
    fig.set_size_inches(8, 4)
    

    axs.plot(corresponding_x_axis, total_signals)
    col2.plotly_chart(fig)

# ------------------------------------------------------------------------------------adding_sin_waves

def adding_sin_waves(frequency,amplitude,df_y_axis,corresponding_x_axis):

    total_signals = df_y_axis
    list_of_objects.append(Signal(frequency=frequency, amplitude=amplitude))
    for object in list_of_objects:
        object_frequency = object.frequency
        object_amplitude = object.amplitude
        signal_y_axis = object_amplitude*sin(2*pi*object_frequency*corresponding_x_axis)
        total_signals += signal_y_axis
    return total_signals

# ------------------------------------------------------------------------------------Removing Signal
def removing_signal(df,removed_freq,removed_amp):

    list_of_columns = df.columns
    df_y_axis = df[list_of_columns[1]]
    corresponding_x_axis = linspace(-1,1, len(df_y_axis))

    total_signals = df_y_axis
    for object in list_of_objects:
        if removed_freq == object.frequency and removed_amp == object.amplitude:
            list_of_objects.remove(object)
            break

    for object in list_of_objects:
        object_frequency = object.frequency
        object_amplitude = object.amplitude
        signal_y_axis = object_amplitude*sin(2*pi*object_frequency*corresponding_x_axis)
        total_signals += signal_y_axis

    return total_signals

# ------------------------------------------------------------------------------------Adding Noise Signal
def add_noise():

    SNR = st.slider(label='SNR', min_value=0.0, max_value=50.0, value=1.0, step=0.1)

    signal_power = total_signals **2                                    # Generating the signal power
    
    signal_power_avg = mean(signal_power)                     # mean of signal power

    if (SNR==0):
        noise_power = signal_power_avg / 0.00001
    else:
        noise_power = signal_power_avg / SNR
    mean_noise = 0
    noise = random.normal(mean_noise,sqrt(noise_power),len(total_signals))
    noise_signal = total_signals + noise

    return noise_signal


# ------------------------------------------------------------------------------------Data Frame Sampling

def signal_sampling(df):

    list_of_columns = df.columns
    global noise
    noise = st.checkbox('Noise')
    if noise:
        df_y_axis=add_noise()
        df_y_axis=list(df_y_axis)
    else:
        df_y_axis = list(df[list_of_columns[1]])
    df_x_axis = list(df[list_of_columns[0]])

    begin_time = df[list_of_columns[0]].iat[0] # begin_time
    end_time = df[list_of_columns[0]].iloc[-1] # end time 

    time_range = abs(begin_time - end_time)

    sample_freq = st.slider(label='Sampling Frequency', min_value=1, max_value=150, step=1)

    sample_rate = int((len(df_x_axis)/time_range)/(sample_freq)) #hakhod sample kol 150 no2ta msln 900pt-- 6 sec 

    if sample_rate == 0:
        sample_rate = 1 #to avoid error of sample_rate approximation to 0

    sampled_time = df_x_axis[::sample_rate] #list from beign to end of x-axis with step of sample Rate
    sampled_amplitude = df_y_axis[::sample_rate] 
    
    return sampled_amplitude, sampled_time , df_y_axis

# ------------------------------------------------------------------------------------Data Frame Reconstructing

def signal_reconstructing(df, sampled_time, sampled_amplitude):

    list_of_columns = df.columns
    time_points = list(df[list_of_columns[0]])
    time_matrix = resize(time_points, (len(sampled_time), len(time_points))) # Matrix containing all Timepoints
    #Pass array of points , number of rows , number of columns to time_matrix
    
    # The following equations is according to White- Shannon interpoltion formula ((t- nT)/T)
    K = (time_matrix.T - sampled_time) / (sampled_time[1] - sampled_time[0]) # Transpose for time_matrix is a must for proper calculations (broadcasting)

    # Reconstructed Amplitude = x[n] sinc(v) -- Whitetaker Shannon
    final_matrix = sampled_amplitude * sinc(K)

    # Summation of columns of the final matrix to get an array of reconstructed points
    reconstructed_signal = sum(final_matrix, axis=1)

    return time_points,reconstructed_signal
