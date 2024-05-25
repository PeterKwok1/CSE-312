key = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def pad_time(string, padding=2):
    string = padding * "0" + str(string)
    return string[-2:]


def add_time(start, duration, day=None):
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

    # end
    end_hour = start_hour + duration_hour
    end_min = start_min + duration_min
    # remainder to next place
    carried_hours = end_min // 60
    end_hour += carried_hours
    end_min = end_min % 60
    carried_days = end_hour // 24
    end_hour = end_hour % 24

    # am or pm
    meridian = "AM" if end_hour < 12 else "PM"
    if end_hour > 12:
        end_hour -= 12
    elif end_hour == 0:
        end_hour = 12

    # first new_time
    new_time = f"{end_hour}:{pad_time(end_min)} {meridian}"

    # optional day of the week
    if day:
        lower_case_key = [day.lower() for day in key]
        start_day_index = lower_case_key.index(day.lower())
        print(lower_case_key, start_day_index)
        days_to_add = carried_days % 7
        # doesn't wrap > 7 (6)
        end_day = key[start_day_index + days_to_add]
        new_time += f", {end_day}"

    # days later
    if carried_days > 0:
        days_later_str = "(next day)"
        if carried_days > 1:
            days_later_str = f"({carried_days} days later)"
        new_time += f" {days_later_str}"

    return new_time


result = add_time("11:59 PM", "24:05", "saturDay")

print(result)
