def format_time(time):
    hours, rem = divmod(time, 3600)
    minutes, seconds = divmod(rem, 60)
    if hours != 0:
        return "%dh %m %.2fs" % (hours, minutes, seconds)
    elif hours == 0 and minutes != 0:
        return "%dm %.2fs" % (minutes, seconds)
    else:
        return "%.2fs" % (seconds)
