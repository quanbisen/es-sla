from datetime import datetime
import pytz


def print_message(message):
    print(str(datetime.now(tz=pytz.timezone('Asia/Shanghai'))) + " " + message)
