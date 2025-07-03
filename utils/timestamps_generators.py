from datetime import datetime
import pytz

def timestamps_gen(beginTime, endTime, date) :
    local_tz = pytz.timezone('America/El_Salvador')

    # Build datetime with local time zone
    dt_inicio_local = local_tz.localize(datetime.strptime(f"{date} {beginTime}", "%Y-%m-%d %H:%M"))
    dt_fin_local = local_tz.localize(datetime.strptime(f"{date} {endTime}", "%Y-%m-%d %H:%M"))

    # Convert to UTC
    dt_inicio_utc = dt_inicio_local.astimezone(pytz.utc)
    dt_fin_utc = dt_fin_local.astimezone(pytz.utc)

    # Obtain timestampos in seconds
    begin_timestamp = int(dt_inicio_utc.timestamp())
    end_timestamp = int(dt_fin_utc.timestamp())

    return begin_timestamp, end_timestamp
