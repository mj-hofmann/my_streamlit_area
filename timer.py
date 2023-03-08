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
import pytz
import streamlit as st

from my_streamlit_area import classes_for_timer as my_timer

st.set_page_config(layout="wide")

# set timezone for all
timezone = pytz.timezone("Europe/Berlin")

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


# https://gist.github.com/dhrrgn/7255361
def human_delta(tdelta):
    """
    Takes a timedelta object and formats it for humans.
    Usage:
        # 149 day(s) 8 hr(s) 36 min 19 sec
        print human_delta(datetime(2014, 3, 30) - datetime.now())
    Example Results:
        23 sec
        12 min 45 sec
        1 hr(s) 11 min 2 sec
        3 day(s) 13 hr(s) 56 min 34 sec
    :param tdelta: The timedelta object.
    :return: The human formatted timedelta
    """
    d = dict(days=tdelta.days)
    d["hrs"], rem = divmod(tdelta.seconds, 3600)
    d["min"], d["sec"] = divmod(rem, 60)

    # define format
    if d["hrs"] == 0:
        fmt = "{min}min {sec}s"
    else:
        fmt = "{hrs}h {min}min {sec}s"

    # return
    return fmt.format(**d)


# %%


async def function_asyc(test, project):

    # init remmaining time
    try:
        timer_remaining_s = project.get_remaining_timer_s_from_now()
    except Exception as e:
        print(e)
        # info
        test.markdown(
            f"""<p>Bitte andere Einstellungen wählen.</p>""",
            unsafe_allow_html=True,
        )
        # return
        return

    # define timer interval
    interval_s = 1

    while timer_remaining_s >= 0:

        # pause zzzZZZ... zzzZZZ...
        ret = await asyncio.sleep(interval_s)  # [s]

        # get human readable timedelte
        t_delta = human_delta(datetime.timedelta(seconds=timer_remaining_s))

        # specify message
        test.markdown(
            f"""<p class="big-font">{t_delta} ...</p>""",
            unsafe_allow_html=True,
        )

        # decrement "timer_remaining_s" if(!) worling hour
        if project.is_now_working_hour():
            # decrease initial timer residue by defined interval
            timer_remaining_s -= interval_s
        else:
            # do nothing
            pass

    st.success("Congrats! All done")

    # return
    return


# You can also use High Level functions Like:
# v = asyncio.run(function_asyc())

# custom coroutine
async def main(test, project):
    # report a message
    print("main coroutine started")
    # create and schedule the task
    task = asyncio.create_task(function_asyc(test, project))
    # wait for the task to complete
    r = await task

    # report a final message
    print("main coroutine done")


# define blank field
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
    value=1.5,
    step=0.25,
)

# get start time and duration in approproate format
project_datetime_start = pd.Timestamp.combine(project_start_date, project_start_time)
# define duration in seconds
project_duration_s = slider_value * 3600

# select days
selected_days = options = st.sidebar.multiselect(
    "Welche Tage werden berücksichtigt?",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
)

# init list
list_of_slots = []

# add slots depending on day selection
if "Monday" in selected_days:
    list_of_slots.append(
        my_timer.WorkingDay("Monday", datetime.time(6, 30), datetime.time(9, 0))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Monday", datetime.time(9, 15), datetime.time(12, 15))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Monday", datetime.time(13, 0), datetime.time(16, 15))
    )
if "Tuesday" in selected_days:
    list_of_slots.append(
        my_timer.WorkingDay("Tuesday", datetime.time(6, 30), datetime.time(9, 0))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Tuesday", datetime.time(9, 15), datetime.time(12, 15))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Tuesday", datetime.time(13, 0), datetime.time(16, 15))
    )
if "Wednesday" in selected_days:
    list_of_slots.append(
        my_timer.WorkingDay("Wednesday", datetime.time(6, 30), datetime.time(9, 0))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Wednesday", datetime.time(9, 15), datetime.time(12, 15))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Wednesday", datetime.time(13, 0), datetime.time(16, 15))
    )
if "Thursday" in selected_days:
    list_of_slots.append(
        my_timer.WorkingDay("Thursday", datetime.time(6, 30), datetime.time(9, 0))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Thursday", datetime.time(9, 15), datetime.time(12, 15))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Thursday", datetime.time(13, 0), datetime.time(16, 15))
    )
if "Friday" in selected_days:
    list_of_slots.append(
        my_timer.WorkingDay("Friday", datetime.time(6, 30), datetime.time(9, 0))
    )
    list_of_slots.append(
        my_timer.WorkingDay("Friday", datetime.time(9, 15), datetime.time(11, 45))
    )

# info
print("============")
print(project_datetime_start)
print(project_duration_s)
print("============")

# init project
project = my_timer.Project(project_datetime_start, project_duration_s, list_of_slots)

# info
st.sidebar.write(
    f"""Beginn am {project.start:%d.%m um %H:%M} Uhr, läuft für {slider_value}h 
    und endet mit Pausen um am {project.end:%d.%m um %H:%M} Uhr.  
    Timer start um: {datetime.datetime.now(timezone):%d.%m %Y, %H:%M Uhr}.
    """
)

try:
    st.sidebar.write(f"Timer startet bei {project.get_remaining_timer_s_from_now()}s.")
except Exception as e:
    print(e)

# time slot info
if st.button("Arbeitszeiten anzeigen"):
    # loop
    for i in project.working_hours:
        st.write(f"{i.dayname}: {i.start} \u21e8 {i.end}")


# start the asyncio program
asyncio.run(main(test, project))

# await(main())
