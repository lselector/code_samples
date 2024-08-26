
"""
# script to create a meeting invite ( .ics file )
# GENERIC
"""

import os, sys, pytz
import datetime as dt
import icalendar as ic

script_directory = os.path.dirname(os.path.abspath(__file__))
print("Script directory:", script_directory)
os.chdir(script_directory)

# provide date and time in EST - and run
organizer = "john.smith@gmail.com"
meetdate = "2023-09-27"
start_dt_EST = f"{meetdate} 13:30:00"
end_dt_EST   = f"{meetdate} 14:00:00"
meeting_name = "meeting"
summary = "Our Group Meeting"
description = """
Our Group Meeting

Use Zoom: 
https://us02web.zoom.us/j/12345abcde
"""
# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------
def convert_est_to_utc(date_time_str):
    """ convert EST date time string into UTC datetime object"""
    eastern = pytz.timezone('US/Eastern')
    dtformat = "%Y-%m-%d %H:%M:%S"
    naive_datetime = dt.datetime.strptime(date_time_str, dtformat)
    localized_datetime = eastern.localize(naive_datetime)
    utc_datetime = localized_datetime.astimezone(pytz.utc)
    return utc_datetime

# --------------------------------------------------------------
# main part
# --------------------------------------------------------------
cal = ic.Calendar()
event = ic.Event()
event.add('organizer', f'mailto:{organizer}')
event.add('summary', summary)

event.add('description', description)

# add as UTC datetime objects
event.add('dtstart', convert_est_to_utc(start_dt_EST))
event.add('dtend'  , convert_est_to_utc(end_dt_EST  ))

# add recurrency if needed
# event.add('rrule', {'freq': 'weekly', 'byday': ['FR']})

cal.add_component(event)

start_dt_EST = start_dt_EST.replace(':','')
start_dt_EST = start_dt_EST.replace('-','')
start_dt_EST = start_dt_EST.replace(' ','_')

fname = script_directory + f'/{meeting_name}_{start_dt_EST}.ics'
with open(fname, 'wb') as f:
    f.write(cal.to_ical())
