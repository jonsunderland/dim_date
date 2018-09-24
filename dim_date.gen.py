from datetime import date, time, datetime, timedelta
import random
import math
import sys
import argparse
import csv

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
    return next_month - timedelta(days=next_month.day)

parser = argparse.ArgumentParser(description="Generating date dimension")
parser.add_argument('--startDate', type=str , default='18000101', help='Start date in YYYYMMDD format', dest='startDate')
parser.add_argument('--endDate', type=str , default='22001231' , help='end date in YYYYMMDD format', dest='endDate')
parser.add_argument('--filename', type=str, default='data/dim_date.csv', help='filename for output', dest='fileName')

argList = parser.parse_args()
print( "Writing to %s" % argList.fileName )

if (((not argList.startDate.isdigit())
    or (not (len(argList.startDate) == 8)))
    or ((not argList.endDate.isdigit())
    or (not (len(argList.endDate) == 8)))
    or (argList.startDate > argList.endDate)):
    print( "Input(s) must be numeric in YYYYMMDD format and end date must not be earlier than start date" )
    sys.exit (1)

try:
    startDate = date(int(argList.startDate[0:4]), int(argList.startDate[4:6]), int(argList.startDate[6:8]))
    endDate = date(int(argList.endDate[0:4]), int(argList.endDate[4:6]), int(argList.endDate[6:8]))
except ValueError:
    print( "Input(s) must be valid date value in YYYYMMDD format" )
    sys.exit (1)
dow=[ 'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

dim_date=[]
yearList=[]
weekList=[]
monthList=[]
while( startDate <= endDate ):
    weekNumber=startDate.strftime('%GW%V')
    if weekNumber not in weekList:
        weekList.append( weekNumber)

    if startDate.strftime('%Y%m') not in monthList:
        monthList.append( startDate.strftime('%Y%m') )

    if startDate.year not in yearList:
        yearList.append( startDate.year )

    days_in_year = (date(startDate.year,12,31)-date(startDate.year,1,1)).days
    days_left_in_year = (date(startDate.year,12,31)-date(startDate.year,1,1)).days - int( startDate.strftime('%j') )
    pct_of_year = float( startDate.strftime('%j') ) / float( days_in_year)
    radians = math.pi/2.0 - ( 2 * math.pi * pct_of_year )
    dateInfo = {
          'dt_id' : len( dim_date ) + 1
        , 'dt_y_m_d': startDate.strftime('%Y-%m-%d')
        , 'dt_year': startDate.strftime('%Y')
        , 'dt_month': startDate.strftime('%m')
        , 'dt_day': startDate.strftime('%j')
        , 'dt_days_in_year' : days_in_year
        , 'dt_day_of_year': startDate.strftime('%j')
        , 'dt_days_left_in_year' : days_left_in_year
        , 'dt_year_start_dt' : startDate.strftime( '%Y-01-01')
        , 'dt_year_end_dt' : startDate.strftime( '%Y-12-31')
        , 'dt_year_month': startDate.strftime('%Y%m')
        , 'dt_month_start_dt': startDate.strftime('%Y-%m-01')
        , 'dt_month_end_dt': last_day_of_month( startDate ).strftime('%Y-%m-%d')
        , 'dt_days_in_month' : last_day_of_month( startDate ).strftime('%d')
        , 'dt_month_name' : startDate.strftime('%B')
        , 'dt_month_name_short' : startDate.strftime('%B')[0:3]
        , 'dt_year_id' : len( yearList)
        , 'dt_month_id' : len( monthList )
        , 'dt_iso_weekday' : startDate.isoweekday()%7
        , 'dt_iso_dow_full' : dow[ startDate.isoweekday()%7 ]
        , 'dt_iso_dow_short' : dow[ startDate.isoweekday()%7 ][0:3]
        , 'dt_is_weekday' : int( startDate.isoweekday()%7 not in [ 5 , 6] )
        , 'dt_is_weekend' : int( startDate.isoweekday()%7 in [ 5 , 6] )
        , 'dt_week_start_dt' : startDate - timedelta( days=startDate.weekday() )
        , 'dt_week_end_dt' : ( startDate - timedelta( days=startDate.weekday() )) + timedelta( days=6)
        , 'dt_iso_weeknumber' : weekNumber
        , 'dt_iso_week_id' : len(weekList)
        , 'dt_pct_of_year' : round( pct_of_year , 2 )
        , 'dt_viz_pct_year_radians' : radians
        , 'dt_viz_pct_x_pos' : math.cos( radians )
        , 'dt_viz_pct_y_pos' : math.sin( radians )
        }
    dim_date.append( dateInfo )
    startDate = startDate + timedelta( days=1)

print( "Date Range from: %s to %s (%d records)" % ( dim_date[0]['dt_y_m_d'] , dim_date[-1]['dt_y_m_d'] , len(dim_date)) )

with open( argList.fileName , 'w') as csvfile:
    writer = csv.DictWriter(csvfile, restval='' , extrasaction='ignore' , fieldnames=dim_date[0].keys())
    writer.writeheader()
    writer.writerows( dim_date )
