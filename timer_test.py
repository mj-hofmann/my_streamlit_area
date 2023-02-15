# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:33:09 2023

@author: LocalAdmin
"""
# %%
import datetime

import pandas as pd


# define working hours
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


# Define working time slots
w1 = WorkingDay("Monday", datetime.time(8, 0), datetime.time(8, 5))
w2 = WorkingDay("Monday", datetime.time(8, 10), datetime.time(8, 12))
w3 = WorkingDay("Monday", datetime.time(8, 15), datetime.time(9, 5))
w4 = WorkingDay("Tuesday", datetime.time(8, 0), datetime.time(8, 5))
w5 = WorkingDay("Tuesday", datetime.time(8, 10), datetime.time(8, 12))
w6 = WorkingDay("Tuesday", datetime.time(8, 15), datetime.time(12, 5))

print(w1.is_now_working_hour(now=datetime.datetime(2023, 2, 13, 8, 3)))

# define start
datetime_start = datetime.datetime(2023, 2, 13, 8, 0, 0)

# define duration in seconds
duration_s = 1.25 * 60 * 60

# init project
project = Project(datetime_start, duration_s, [w1, w2, w3, w4, w5, w6])

schedule = project.get_working_slots()

# get of project time
dt_proj_end = project.end
