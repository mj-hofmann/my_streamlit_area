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


class WorkingDay:
    def __init__(
        self, day_of_name: str, start_time: datetime.time, end_time: datetime.time
    ):

        self.dayname = day_of_name
        self.start = start_time
        self.end = end_time

    def is_now_working_hour(self, now=None) -> bool:
        # check of now is within working hours
        if not now:
            # get current time
            now = datetime.datetime.now()

        # get "time" corresponding to now
        now = datetime.time(now.hour, now.minute, now.second)

        if (now >= self.start) and (now <= self.end):
            return True
        else:
            return False


class Project:

    end = None

    def __init__(
        self, start: datetime.datetime, duration_s: int, working_hours: list[WorkingDay]
    ):

        self.start = start
        self.duration_s = duration_s
        self.working_hours = working_hours

        # call calculation of project end time on init
        self.get_end()

    def get_working_slots(self):

        # init lists
        list_of_tuples = [
            # (self.start, "START==="),
            # (self.start + datetime.timedelta(seconds=self.duration_s), "END NAIVE==="),
        ]

        for slot in self.working_hours:

            for delta_d in range(7 + 1):

                if (self.start + datetime.timedelta(delta_d)).strftime(
                    "%A"
                ) == slot.dayname:
                    # get intervals
                    list_of_tuples.append(
                        (
                            datetime.datetime.combine(
                                self.start + datetime.timedelta(delta_d), slot.start
                            ),
                            "start",
                        )
                    )
                    list_of_tuples.append(
                        (
                            datetime.datetime.combine(
                                self.start + datetime.timedelta(delta_d), slot.end
                            ),
                            "end",
                        )
                    )

        # to dataframe
        schedule = pd.DataFrame(list_of_tuples, columns=["datetime", "type"])

        # sort
        schedule = schedule.sort_values(by="datetime")

        # return
        return schedule

    def get_end(self):

        # get working slots
        helper = self.get_working_slots()

        # set index column
        helper["index"] = helper["type"]
        helper = helper.set_index("index")

        # add auxiliary columns
        shift_by = -1
        helper["type2"] = helper["type"].shift(shift_by)
        helper["datetime2"] = helper["datetime"].shift(shift_by)

        # get timedelta
        helper["timedelta_s"] = (
            helper["datetime2"] - helper["datetime"]
        ).dt.total_seconds()

        # get working time slot duration
        helper = helper[(helper["type"] == "start") & (helper["type2"] == "end")]

        # cumulative working time
        helper["cumlative_working_time_s"] = helper["timedelta_s"].cumsum()

        # remaining
        helper["remaining_s"] = self.duration_s - helper["cumlative_working_time_s"]

        # end date
        helper = helper.query("remaining_s <= 0").head(1)

        # get end time time based on remaining time
        dt_end = helper["datetime2"] + datetime.timedelta(
            seconds=int(helper["remaining_s"])
        )

        # save as attribute
        self.end = dt_end.tolist()[0]

        # return
        return self.end

    # @pysnooper.snoop()
    def is_now_working_hour(self, now=None) -> bool:
        # loop all slots
        for i in self.working_hours:
            # check for this day
            if i.dayname != now.strftime("%A"):
                # go to next
                continue

            # "else": check for this slot
            if i.is_now_working_hour(now):
                # return
                return True

        # default: return false
        return False


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

    st.success("Congrats! All done")

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
