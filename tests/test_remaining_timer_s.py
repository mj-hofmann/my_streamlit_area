import datetime

import pytest

from my_streamlit_area import classes_for_timer as cs


@pytest.mark.parametrize(
    "duration_h",
    [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6],
)
def test_project_end(duration_h):
    # init list
    list_of_slots = [
        cs.WorkingDay("Monday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Monday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Monday", datetime.time(13, 0), datetime.time(16, 15)),
        cs.WorkingDay("Tuesday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Tuesday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Tuesday", datetime.time(13, 0), datetime.time(16, 15)),
        cs.WorkingDay("Wednesday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Wednesday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Wednesday", datetime.time(13, 0), datetime.time(16, 15)),
        cs.WorkingDay("Thursday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Thursday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Thursday", datetime.time(13, 0), datetime.time(16, 15)),
    ]

    # define start (SUNDAY) --> remaining time = project duration
    project_datetime_start = datetime.datetime(2023, 2, 26, 8, 15)

    # define duration
    project_duration_s = duration_h * 3600  # [s]

    # init project
    project = cs.Project(
        project_datetime_start,
        project_duration_s,
        list_of_slots,
    )

    # check
    assert (
        project.get_remaining_timer_s_from_now(now=project_datetime_start)
        == project_duration_s
    )


@pytest.mark.parametrize(
    "duration_h",
    [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6],
)
def test_project_end_later_now(duration_h):
    # init list
    list_of_slots = [
        cs.WorkingDay("Monday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Monday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Monday", datetime.time(13, 0), datetime.time(16, 15)),
        cs.WorkingDay("Tuesday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Tuesday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Tuesday", datetime.time(13, 0), datetime.time(16, 15)),
        cs.WorkingDay("Wednesday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Wednesday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Wednesday", datetime.time(13, 0), datetime.time(16, 15)),
        cs.WorkingDay("Thursday", datetime.time(6, 30), datetime.time(9, 0)),
        cs.WorkingDay("Thursday", datetime.time(9, 15), datetime.time(12, 15)),
        cs.WorkingDay("Thursday", datetime.time(13, 0), datetime.time(16, 15)),
    ]

    # define start (MONDAY) --> remaining time = project duration
    project_datetime_start = datetime.datetime(2023, 2, 27, 6, 30)

    # define duration
    project_duration_s = duration_h * 3600  # [s]

    # init project
    project = cs.Project(
        project_datetime_start,
        project_duration_s,
        list_of_slots,
    )

    # check
    assert (
        project.get_remaining_timer_s_from_now(
            now=project_datetime_start + datetime.timedelta(minutes=30)
        )
        == project_duration_s - 30 * 60
    )
