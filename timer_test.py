# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:33:09 2023

@author: LocalAdmin
"""
# %%
import datetime

import pandas as pd

# define start
datetime_start = datetime.datetime(2023, 2, 13, 8, 0, 0)

# define duration in seconds
duration_s = 2.25 * 60 * 60

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


w1 = WorkingDay("Monday", datetime.time(8, 0), datetime.time(8, 5))
w2 = WorkingDay("Monday", datetime.time(8, 10), datetime.time(8, 12))
w3 = WorkingDay("Monday", datetime.time(8, 15), datetime.time(9, 5))
w4 = WorkingDay("Tuesday", datetime.time(8, 0), datetime.time(8, 5))
w5 = WorkingDay("Tuesday", datetime.time(8, 10), datetime.time(8, 12))
w6 = WorkingDay("Tuesday", datetime.time(8, 15), datetime.time(12, 5))

print(w1.is_now_working_hour(now=datetime.datetime(2023, 2, 13, 8, 3)))


# %%

# get navive end
datetime_end = datetime_start + datetime.timedelta(seconds=duration_s)


class Project:
    def __init__(self, start: datetime.datetime, duration_s: int, working_hours: list):

        self.start = start
        self.duration_s = duration_s
        self.working_hours = working_hours

    def get_working_slots(self):

        # init lists
        list_of_tuples = [
            (self.start, "START==="),
            (self.start + datetime.timedelta(seconds=self.duration_s), "END NAIVE==="),
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


project = Project(datetime_start, duration_s, [w1, w2, w3, w4, w5, w6])

schedule = project.get_working_slots()
