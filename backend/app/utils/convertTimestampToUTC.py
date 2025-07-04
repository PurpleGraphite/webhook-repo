from datetime import datetime, timezone

def convertTimestampToUTC(timestamp):
    dt = datetime.fromisoformat(timestamp)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    utc_iso_str = datetime.isoformat(dt).replace('+00:00', 'Z')
    return  utc_iso_str