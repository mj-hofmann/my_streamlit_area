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


async def function_asyc():
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
        await asyncio.sleep(interval_s)  # [s]

        # dscrease remaining time
        duration_remaining -= interval_s

        test.markdown(
            f"""<p class="big-font">{duration_remaining:.1f}s remaining</p>""",
            unsafe_allow_html=True,
        )

        # info
        print(f"{duration_remaining}s remaining")

    st.success("Congrats! All done", icon="🔥")

    # return
    return


# You can also use High Level functions Like:
# v = asyncio.run(function_asyc())

# custom coroutine
async def main():
    # report a message
    print("main coroutine started")
    # create and schedule the task
    task = asyncio.create_task(function_asyc())
    # wait for the task to complete
    await task

    # report a final message
    print("main coroutine done")


test = st.empty()

slider_value = st.sidebar.slider("duration", min_value=1, max_value=10, value=7)

# start the asyncio program
asyncio.run(main())

# await(main())
