from cli.helpers.time_helpers import format_time


def test_format_time_only_seconds():
    time_str = format_time(2.222)
    assert time_str == "2.22s"


def test_format_time_only_minutes():
    time_str = format_time(120.000)
    assert time_str == "2m 0.00s"


def test_format_time_only_hours():
    time_str = format_time(7200.000)
    assert time_str == "2h 0m 0.00s"


def test_format_time_minutes_seconds():
    time_str = format_time(122.222)
    assert time_str == "2m 2.22s"


def test_format_time_hours_minutes_seconds():
    time_str = format_time(7322.222)
    assert time_str == "2h 2m 2.22s"
