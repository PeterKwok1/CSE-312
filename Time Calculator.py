def pad(str, padding):
    str = padding * "0" + str
    return str[-2:]


def add_time(start, duration):
    start = start.split(" ")
    start_time = start[0].split(":")
    start_hour = int(start_time[0])
    start_min = int(start_time[1])
    am_pm = start[1]
    # 24 hour format
    if am_pm == "PM":
        start_hour += 12

    duration = duration.split(":")
    duration_hour = int(duration[0])
    duration_min = int(duration[1])

    # start + duration
    start_hour += duration_hour
    start_min += duration_min
    # remainder to next place
    carried_hours = start_min // 60
    start_hour += carried_hours
    start_min = start_min % 60
    carried_days = start_hour // 24
    start_hour = start_hour % 24

    # am or pm
    meridian = "AM" if start_hour < 12 else "PM"
    print(carried_days, start_hour, start_min, meridian)
    # convert to string before padding

    # return new_time


add_time("10:40 PM", "3:30")
