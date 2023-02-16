# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:33:09 2023

@author: LocalAdmin
"""
# %%
import datetime

import pandas as pd
import pysnooper


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
            (self.start, "START==="),
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

        # use "START===" as beginning
        helper = helper.loc["START===":, :]
        # rename
        helper["type"] = helper["type"].str.replace("START===", "start")

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

    def get_remaining_timer_s_from_now(self, now=None):
        # what to use as now?
        if not now:
            # use current time
            now = datetime.datetime.now()

        # get working slots
        helper = self.get_working_slots()

        # append "NOW" and "END" information
        helper = pd.concat(
            [
                helper,
                pd.DataFrame({"datetime": now, "type": "NOW"}, index=[0]),
                pd.DataFrame({"datetime": project.end, "type": "END==="}, index=[0]),
            ]
        ).sort_values(by="datetime")

        # set index column
        helper["index"] = helper["type"]
        helper = helper.set_index("index")

        # use "START===" as beginning
        helper = helper.loc["NOW":"END===", :]
        # rename
        helper["type"] = helper["type"].str.replace("NOW", "start")

        # add auxiliary columns
        shift_by = -1
        helper["type2"] = helper["type"].shift(shift_by)
        helper["datetime2"] = helper["datetime"].shift(shift_by)

        # get timedelta
        helper["timedelta_s"] = (
            helper["datetime2"] - helper["datetime"]
        ).dt.total_seconds()

        helper["type"] = helper["type"].str.replace("END===", "end")
        helper["type2"] = helper["type2"].str.replace("END===", "end")

        # get working time slot duration
        helper = helper[(helper["type"] == "start") & (helper["type2"] == "end")]

        # # cumulative working time
        timer_s_from_now = int(helper["timedelta_s"].cumsum())

        # return
        return timer_s_from_now

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


# Define working time slots
w1 = WorkingDay("Monday", datetime.time(8, 0), datetime.time(8, 30))
w2 = WorkingDay("Monday", datetime.time(9, 0), datetime.time(9, 30))
w3 = WorkingDay("Monday", datetime.time(10, 0), datetime.time(14, 0))
w4 = WorkingDay("Tuesday", datetime.time(8, 0), datetime.time(8, 5))
w5 = WorkingDay("Tuesday", datetime.time(8, 10), datetime.time(8, 12))
w6 = WorkingDay("Tuesday", datetime.time(8, 15), datetime.time(12, 5))

print(w1.is_now_working_hour(now=datetime.datetime(2023, 2, 13, 8, 3)))

# define start
datetime_start = datetime.datetime(2023, 2, 13, 8, 5, 0)

# define duration in seconds
duration_s = 0.5 * 60 * 60

# init project
project = Project(datetime_start, duration_s, [w1, w2, w3, w4, w5, w6])

schedule = project.get_working_slots()

# get of project time
dt_proj_end = project.end

# check
print(project.is_now_working_hour(now=datetime.datetime(2023, 2, 13, 8, 0)))


# %% get remaining active seconds

now_mock = datetime.datetime(2023, 2, 13, 9, 2)

rem_s = project.get_remaining_timer_s_from_now(now=now_mock)


# %%

rem_s = 3000


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

    if d["min"] == 0:
        fmt = "{sec} sec"
    elif d["hrs"] == 0:
        fmt = "{min} min {sec} sec"
    elif d["days"] == 0:
        fmt = "{hrs} hr(s) {min} min {sec} sec"
    else:
        fmt = "{days} day(s) {hrs} hr(s) {min} min {sec} sec"

    return fmt.format(**d)


dt_delta = datetime.timedelta(seconds=rem_s)

print(human_delta(dt_delta))
