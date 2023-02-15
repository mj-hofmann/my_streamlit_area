# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 16:48:30 2023
 
@author: HofmanMJ
 
https://discuss.streamlit.io/t/issue-with-asyncio-run-in-streamlit/7745/11
"""
# %%
# %%
import asyncio
import datetime

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .big-font {
        font-size: 130px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# @pysnooper.snoop()
def is_in_time_range(
    check_datetime: datetime.datetime, start: datetime.time, end: datetime.time
) -> bool:
    # info
    print("is_in_time_range")

    check_time = datetime.time(check_datetime.hour, check_datetime.minute)

    if check_time >= start and check_time <= end:
        return True
    else:
        return False


# check
vlaid = is_in_time_range(
    datetime.datetime.now(), datetime.time(19, 0), datetime.time(20, 15)
)

# %%


async def function_asyc(test):
    # define starttime
    dt_start = datetime.datetime.now()
    print(dt_start)

    #    duration = 10  # [s]
    duration = slider_value

    # init remmaining time
    duration_remaining = duration

    today_name = datetime.date.today().strftime("%A")
    print(today_name)

    interval_s = 0.1

    while duration_remaining >= 0:
        print(datetime.date.today())
        ret = await asyncio.sleep(interval_s)  # [s]

        # dscrease remaining time
        duration_remaining -= interval_s

        test.markdown(
            f"""<p class="big-font">{duration_remaining:.0f}s left</p>""",
            unsafe_allow_html=True,
        )

        # info
        print(f"{duration_remaining}s left")

    st.success("Congrats! All done", icon="🔥")

    # return
    return


# You can also use High Level functions Like:
# v = asyncio.run(function_asyc())

# custom coroutine
async def main(test):
    # report a message
    print("main coroutine started")
    # create and schedule the task
    task = asyncio.create_task(function_asyc(test))
    # wait for the task to complete
    r = await task

    # report a final message
    print("main coroutine done")


test = st.empty()

# define start date
project_start_date = st.sidebar.date_input(
    "Wann beginnt der Takt?", datetime.date.today()
)

# define start time
project_start_time = st.sidebar.time_input("Startzeit", datetime.time(8, 0))

# define project duration
slider_value = st.sidebar.slider(
    "Wie lange dauert der Takt in Stunden",
    min_value=1.0,
    max_value=10.0,
    value=3.0,
    step=0.25,
)

# get start time and duration in approproate format
project_datetime_start = pd.Timestamp.combine(project_start_date, project_start_time)
# define duration in seconds
project_duration_s = slider_value * 3600

# info
st.sidebar.write(f"Beginn am {project_datetime_start:%A, %H:%M} für {slider_value}h.")

# start the asyncio program
asyncio.run(main(test))

# await(main())
