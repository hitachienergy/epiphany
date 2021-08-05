from math import floor

def format_time(secs):
    """Formats seconds to a time string with the format: "Xh Xm X.XXs", "Xm X.XXs", "X.XXs"

    Parameters:
    secs (float): Time in seconds

    Returns:
    string: Formatted time string
   """

    seconds = secs%60
    minutes = floor((secs/60)%60)
    hours = floor(secs/(60*60)%24)
    if hours != 0:
        return "%dh %dm %.2fs" % (hours, minutes, seconds)
    elif hours == 0 and minutes != 0:
        return "%dm %.2fs" % (minutes, seconds)
    else:
        return "%.2fs" % (seconds)
