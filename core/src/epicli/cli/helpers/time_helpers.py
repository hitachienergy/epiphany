from math import floor

def format_time(time):
    seconds = time%60
    minutes = floor((time/60)%60)
    hours = floor(time/(60*60)%24)
    if hours != 0:
        return "%dh %dm %.2fs" % (hours, minutes, seconds)
    elif hours == 0 and minutes != 0:
        return "%dm %.2fs" % (minutes, seconds)
    else:
        return "%.2fs" % (seconds)
