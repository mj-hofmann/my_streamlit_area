# %%
import datetime

from my_streamlit_area import classes_for_timer as my_timer

# init list
list_of_slots = [
    my_timer.WorkingDay("Monday", datetime.time(6, 30), datetime.time(9, 0)),
    my_timer.WorkingDay("Monday", datetime.time(9, 15), datetime.time(12, 15)),
    my_timer.WorkingDay("Monday", datetime.time(13, 0), datetime.time(16, 15)),
    my_timer.WorkingDay("Tuesday", datetime.time(6, 30), datetime.time(9, 0)),
    my_timer.WorkingDay("Tuesday", datetime.time(9, 15), datetime.time(12, 15)),
    my_timer.WorkingDay("Tuesday", datetime.time(13, 0), datetime.time(16, 15)),
    my_timer.WorkingDay("Wednesday", datetime.time(6, 30), datetime.time(9, 0)),
    my_timer.WorkingDay("Wednesday", datetime.time(9, 15), datetime.time(12, 15)),
    my_timer.WorkingDay("Wednesday", datetime.time(13, 0), datetime.time(16, 15)),
    my_timer.WorkingDay("Thursday", datetime.time(6, 30), datetime.time(9, 0)),
    my_timer.WorkingDay("Thursday", datetime.time(9, 15), datetime.time(12, 15)),
    my_timer.WorkingDay("Thursday", datetime.time(13, 0), datetime.time(16, 15)),
]

# define start
project_datetime_start = datetime.datetime(2023, 2, 26, 8, 15)

# define duration
project_duration_s = 4 * 3600  # [s]


# info
print("============")
print(project_datetime_start)
print(project_duration_s)
print("============")

# init project
project = my_timer.Project(project_datetime_start, project_duration_s, list_of_slots)

# get end
ret_end = project.get_end()
print(f"Ends at {ret_end}")

ret_rem_time = project.get_remaining_timer_s_from_now(
    # now=datetime.datetime(2023, 2, 26, 8, 15)
    now=datetime.datetime(2023, 2, 27, 7, 30)
)
print(f"Remaining {ret_rem_time}s")

project.is_now_working_hour(datetime.datetime.now())
