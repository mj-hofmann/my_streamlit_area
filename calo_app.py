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
xlim_low_peaks_onset = st.sidebar.slider("Discarded s for peaks and onset", 1, 10000, 300)

# # File uploader
# uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=True)


# init object
text_input_path = st.text_input(
    "Path",
    # value=r"C:\Users\LocalAdmin\Documents\GitHub\TAInstCalorimetry\DATA"
    )


@st.cache
def load_and_init(xlim):
    # init object
    calos = tacalorimetry.Measurement(folder=text_input_path)
    
    # restrict x range
    calos._data = calos.get_data().query("time_s <= @xlim")
    
    # short names
    calos._data["sample"] = [Path(i).stem for i in calos._data["sample"]]
    
    return calos
  
calos = load_and_init(xlim)
    
# add samples to sidebar
multiselect_sample= st.sidebar.multiselect(
    "samples",
    calos.get_data()["sample"].unique(),  # options
    calos.get_data()["sample"].unique(),  # selected
    )
    
calos.plot()
    

fig = plt.figure(figsize=(10, 4))

# plot
p = sns.lineplot(
    data=calos.get_data()[
        calos.get_data()["sample"].str.match(
        "(" + ")|(".join(multiselect_sample) + ")"
        )
    ].iloc[::10,:],
    x="time_s",
    y="normalized_heat_flow_w_g",
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
    peaks = calos.get_peaks()
    
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
st.text(f"Discarding data points before {xlim_low_peaks_onset} s.")
   

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
    )

fig = px.scatter(
    peaks_and_onsets,
    x="time_s_x",
    y="time_s_y",
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