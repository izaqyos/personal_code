#!/opt/homebrew/bin/python3

import pendulum
now_israel = pendulum.now("Asia/Jerusalem") 
print(f"now in israel {now_israel}")

same_time_in_other_tz = now_israel.in_timezone('UTC')
print(f"same now of israel in UTC {same_time_in_other_tz}")

tomorrow = pendulum.now().add(days=1)
last_week = pendulum.now().subtract(weeks=1)
print(f"tomorrow={tomorrow}, last_week={last_week}")


past = pendulum.now().subtract(minutes=2)
print(f"past 2 minuts: {past.diff_for_humans()}")

delta = past - last_week

print(f"delta in hours={delta.hours}, delta in words={delta.in_words(locale='en')}")

## Proper handling of datetime normalization
#>>> pendulum.datetime(2013, 3, 31, 2, 30, tz='Europe/Paris')
#'2013-03-31T03:30:00+02:00' # 2:30 does not exist (Skipped time)
#
## Proper handling of dst transitions
#>>> just_before = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999, tz='Europe/Paris')
#'2013-03-31T01:59:59.999999+01:00'
#>>> just_before.add(microseconds=1)
#'2013-03-31T03:00:00+02:00'


