from datetime import timedelta,datetime


def parse_duration(duration_str):
    duration_str = duration_str.replace("P", "").replace("T", "")

    components = ["D", "H", "M", "S"]
    values = {"D": 0, "H": 0, "M": 0, "S": 0}

    for component in components:
        if component in duration_str:

            # 10H30M , after splitting by H(component) -> value = 10 and duration_str = 30M
            value, duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(
        days=values["D"], hours=values["H"], minutes=values["M"], seconds=values["S"]
    )
    return total_duration

    # eg -> t=timedelta(days = 1, hours = 10, minutes = 30) -> print(t)-> 1 day, 10:30:00


def transform_data(row):
    duration_td = parse_duration(row["Duration"])#is a timedelta

    #we cannot directly convert timedelta to time hence we add datetime.min to duration_td and then extract only time part
    row["Duration"] = (datetime.min + duration_td).time()#datetime.min -> minimum datetime value (0001-01-01 00:00:00)
    row["Video_Type"] = "Shorts" if duration_td.total_seconds() <= 60 else "Normal"
    return row