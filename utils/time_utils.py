from datetime import datetime
import pytz # type: ignore

def format_time(timestamp, timezone='America/Santiago'):
    return datetime.fromtimestamp(timestamp, pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S')
