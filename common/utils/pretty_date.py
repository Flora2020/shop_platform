def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like '1 小時前', '昨天', '3 個月前',
    '剛剛', etc
    """
    from datetime import datetime
    now = datetime.now()
    diff = None
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return '剛剛'
        if second_diff < 60:
            return str(second_diff) + ' 秒前'
        if second_diff < 120:
            return '1 分鐘前'
        if second_diff < 3600:
            return str(second_diff // 60) + ' 分鐘前'
        if second_diff < 7200:
            return '1 小時前'
        if second_diff < 86400:
            return str(second_diff // 3600) + ' 小時前'
    if day_diff == 1:
        return '昨天'
    if day_diff < 7:
        return str(day_diff) + ' 天前'
    if day_diff < 31:
        return str(day_diff // 7) + ' 周前'
    if day_diff < 365:
        return str(day_diff // 30) + ' 個月前'
    return str(day_diff // 365) + ' 年前'

# I found the original code at https://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
