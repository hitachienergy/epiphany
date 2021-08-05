from math import floor

def format_time(seconds):
    """Formats seconds to a time string with the format: "Xh Xm X.XXs", "Xm X.XXs", "X.XXs"

    Parameters:
    seconds (float): Time in seconds

    Returns:
    string: Formatted time string
   """

    secs = seconds%60
    minutes = floor((seconds/60)%60)
    hours = floor(seconds/(60*60)%24)
    if hours != 0:
        return "%dh %dm %.2fs" % (hours, minutes, secs)
    elif hours == 0 and minutes != 0:
        return "%dm %.2fs" % (minutes, secs)
    else:
        return "%.2fs" % (secs)
