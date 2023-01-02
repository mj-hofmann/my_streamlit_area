# %%

import streamlit as st
from TAInstCalorimetry import tacalorimetry
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_icon="📈", page_title="Calo Dashboard")

# title
st.title("Calo Dashboard")

# slider in sidebar
xlim = st.sidebar.slider("Cutoff", 1, 1000000, 100000)
xlim_low_peaks_onset = st.sidebar.slider("Discarded s for peaks and onset", 1, 1800, 300)

# File uploader
uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)


# init object
calos = tacalorimetry.Measurement()

# @st.cache
def load_and_init(uploaded_files):
    for file in uploaded_files:
        # consider only xls
        if file.name.endswith(".xls"):
            # # info
            # st.write(file)
            
            # read file from upload        
            this_data = calos._read_calo_data_xls(file.getvalue())
            
        # elif file.name.endswith(".csv"):
        #     # # info
        #     # st.write(file)
            
        #     # read file from upload        
        #     this_data = calos._read_calo_data_csv(file)
            
        else:
            continue
            
        # add sample name
        this_data["sample"] = file.name
        
        # # d = pd.read_excel(file)
        # st.write(this_data.head())
        
        # append
        calos._data = pd.concat([
            calos.get_data(),
            this_data
            ])
            
if uploaded_files and not calos.get_data().empty:          

    # load on update
    load_and_init(uploaded_files)
        
    # restrict x range
    calos._data = calos.get_data().query("time_s <= @xlim")
    calos._data = calos.get_data().query("time_s >= @xlim_low_peaks_onset")
        
    
    # names
    sidebar_columns = st.sidebar.selectbox(
        "Columns",
        calos.get_data().columns[1:-1],
        3
        )
    
    # info
    st.sidebar.write(f"{len(calos.get_data())} data rows.")
    
    # short names
    calos._data["sample"] = [Path(i).stem for i in calos._data["sample"]]
        
    #     return calos
      
    # calos = load_and_init(xlim)
        
    # add samples to sidebar
    multiselect_sample= st.sidebar.multiselect(
        "samples",
        calos.get_data()["sample"].unique(),  # options
        calos.get_data()["sample"].unique(),  # selected
        )    
    
    # init figure
    fig = plt.figure(figsize=(10, 4))
    
    # plot
    p = sns.lineplot(
        data=calos.get_data()[
            calos.get_data()["sample"].str.match(
            "(" + ")|(".join(multiselect_sample) + ")"
            )
        ].iloc[::10,:],
        x="time_s",
        y=sidebar_columns,
        hue="sample"
        )
    
    ax = plt.gca()
    ax.set_ylim(0, 0.005)
    
    # show figure
    st.pyplot(fig)
    
    
    # get pekas and onsets
    @st.cache
    def get_peaks_and_onsets(xlim_low_peaks_onset):
        
        # get peaks
        peaks = calos.get_peaks(
            prominence=0.000005
            )
        
        # sort out peaks
        peaks = peaks.query("time_s >= @xlim_low_peaks_onset")
        
        # get peaks
        onsets = calos.get_peak_onsets(
            time_discarded_s=xlim_low_peaks_onset,
            rolling=1,
            gradient_threshold=0.000002,    
            )
        
        return peaks, onsets
    
    peaks, onsets = get_peaks_and_onsets(xlim_low_peaks_onset)
    
    # Peaks section
    st.header("Peaks")
    
    # Info
    st.text(f"Discarding peaks occurring before {xlim_low_peaks_onset} s.")
       
    
    st.write(peaks[["sample", "time_s"]])
    
    # Onsets section
    st.header("Onsets")
    
    # Info
    st.text(f"Discarding data points before {xlim_low_peaks_onset} s.")
    
    
    
    checkox_onsets = st.checkbox("First onset only", value=True)
    
    if checkox_onsets:
    
        st.write(onsets.drop_duplicates(subset=["sample"], keep="first")[["sample", "time_s", "gradient"]])
        
    else:
        
        st.write(onsets[["sample", "time_s", "gradient"]])
    
    st.header("Plotly chart")
    
    # merge params
    
    peaks_and_onsets = pd.merge(
        peaks,
        onsets.drop_duplicates(subset=["sample"], keep="first"),
        left_on="sample",
        right_on="sample",
        suffixes=("_peak", "_onset")
        )
    
    fig = px.scatter(
        peaks_and_onsets,
        x="time_s_peak",
        y="time_s_onset",
        hover_name="sample"
        )
    
    st.plotly_chart(fig, theme=None, use_container_width=True)
    # st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    
    # @st.cache
    # def convert_df(df):
    #     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #     return df.to_csv().encode('utf-8')
    
    # csv = convert_df(peaks_and_onsets)
    
    # st.download_button(
    #     label="Download data as CSV",
    #     data=csv,
    #     file_name='large_df.csv',
    #     mime='text/csv',
    # )
    
else:
    st.write("Select files xls only (test) ...")