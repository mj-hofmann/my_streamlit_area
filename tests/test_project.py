import datetime

import pytest

from my_streamlit_area import classes_for_timer as cs


@pytest.mark.parametrize(
    "dt_start, duration_h, dt_end",
    [
        (
            str(datetime.datetime(2023, 2, 13, 8, 0)),
            0.25,
            str(datetime.datetime(2023, 2, 13, 8, 15)),
        ),
        (
            str(datetime.datetime(2023, 2, 13, 8, 0)),
            0.50,
            str(datetime.datetime(2023, 2, 13, 8, 30)),
        ),
        (
            str(datetime.datetime(2023, 2, 13, 8, 0)),
            0.75,
            str(datetime.datetime(2023, 2, 13, 9, 15)),
        ),
        (
            str(datetime.datetime(2023, 2, 13, 8, 0)),
            1.00,
            str(datetime.datetime(2023, 2, 13, 9, 30)),
        ),
        (
            str(datetime.datetime(2023, 2, 13, 8, 0)),
            2.00,
            str(datetime.datetime(2023, 2, 13, 12, 30)),
        ),
        (
            str(datetime.datetime(2023, 2, 13, 8, 15)),
            0.25,
            str(datetime.datetime(2023, 2, 13, 8, 30)),
        ),
        (
            str(datetime.datetime(2023, 2, 13, 8, 15)),
            0.50,
            str(datetime.datetime(2023, 2, 13, 9, 15)),
        ),
    ],
)
def test_project_end(dt_start, duration_h, dt_end):
    # Define working time slots
    w1 = cs.WorkingDay("Monday", datetime.time(8, 0), datetime.time(8, 30))
    w2 = cs.WorkingDay("Monday", datetime.time(9, 0), datetime.time(10, 0))
    w3 = cs.WorkingDay("Monday", datetime.time(12, 0), datetime.time(16, 0))
    w4 = cs.WorkingDay("Tuesday", datetime.time(8, 0), datetime.time(8, 30))
    w5 = cs.WorkingDay("Tuesday", datetime.time(9, 0), datetime.time(10, 0))
    w6 = cs.WorkingDay("Tuesday", datetime.time(12, 0), datetime.time(16, 0))

    project_duration_s = duration_h * 3600

    # init project
    project = cs.Project(
        datetime.datetime.fromisoformat(dt_start),
        project_duration_s,
        [w1, w2, w3, w4, w5, w6],
    )

    # check
    assert datetime.datetime.fromisoformat(dt_end) == project.get_end()
