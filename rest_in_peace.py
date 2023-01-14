#! /usr/local/bin/python3.9

import os,sys
import arrow
import random
import datetime
import argparse
from subprocess import *
from setup_logger import *
import pprint

import requests
from requests.exceptions import HTTPError

# Bokeh color reference here:
# https://docs.bokeh.org/en/latest/docs/reference/colors.html
from bokeh.plotting import figure, output_file, show
from bokeh.models import NumeralTickFormatter

# ____________________________________________________________
rip_url = 'https://www.rip.ie/deathnotices.php'
counties = [
    'antrim','armagh','carlow','cavan','clare',
    'cork','derry','donegal','down','dublin',
    'fermanagh','galway','kerry','kildare',
    'kilkenny','laois','leitrim','limerick',
    'longford','louth','mayo','meath',
    'monaghan','offaly','roscommon','sligo',
    'tipperary','tyrone','waterford','westmeath',
    'wexford','wicklow'
]
six_counties = ['antrim','armagh','down','derry','fermanagh','tyrone']
republic_counties = list (set(counties)-set(six_counties))

# --------------------------------------------------------------
params = {
    'do': 'get_deathnotices_pages',
    'sEcho':'8',
    'iColumns':'5',
    'sColumns':'',
    'iDisplayStart':'0',
    'iDisplayLength':'10000',
    'mDataProp_0':'0',
    'mDataProp_1':'1',
    'mDataProp_2':'2',
    'mDataProp_3':'3',
    'mDataProp_4':'4',
    'iSortingCols':'2',
    'iSortCol_0':'0',
    'sSortDir_0':'desc',
    'iSortCol_1':'0',
    'sSortDir_1':'asc',
    'bSortable_0':'true',
    'bSortable_1':'true',
    'bSortable_2':'true',
    'bSortable_3':'true',
    'bSortable_4':'true',
    'CountyID': '29',
    'iDisplayLength':'10000',
    'DateFrom':'2020-04-01 00:00:00',
    'DateTo':'2020-04-05 23:59:59',
    'NoWhere': 'y',
    'include_fn':'false'
}
# _________________________________________________________________________________________
def get_fatalities_for_period (year=None, month=None,target_counties=republic_counties):
    if not year:
        year = arrow.utcnow().year # Current year
    if month:
        fmt1 = 'YYYY-MMM-DD'
        fmt2 = 'YYYY-MM-DD'
        d1  = arrow.get(f'{year}-{month}-01',fmt1)
        month_start = d1.format(fmt2)
        month_end = d1.ceil('month').format(fmt2)

        params['DateFrom'] = f'{month_start} 00:00:00'
        params['DateTo'] = f'{month_end} 23:59:59'
    else:
        params['DateFrom'] = f'{year}-01-01  00:00:00'
        params['DateTo'] = f'{year}-12-31 23:59:59'

    total = 0
    for county in target_counties:
        params['CountyID'] = counties.index(county)+1
        response = requests.get(
            rip_url,
            params=params
        )
        rdata = response.json()
        dcount = rdata['iTotalRecords']
        total += int(dcount)
    return total

# _____________________________________________________________________________________________________________
def main():
    parser = argparse.ArgumentParser(description='This does cool stuff man!')
    parser.add_argument('--county',help='Results for the given county (name in lowercase)')
    parser.add_argument('--yrmonth',help='Deaths for specified month of year (in YYYY-MMM format (e.g 2021-Jun))')
    parser.add_argument('--year',help='Deaths for specified  year (in YYYY format (e.g 2021))')
    parser.add_argument('--plot', action="store_true"),
    parser.add_argument('--debug', action="store_true",
                        help='Run in debug mode')
    args = parser.parse_args()
    # ----------------------------------
    target_counties = republic_counties
    if args.county:
        target_counties = [args.county]
    # -----------------------------------
    if not args.plot:
        if args.yrmonth:
            fields = args.yrmonth.split('-')
            year = fields[0]
            month = fields[1]
            total = get_fatalities_for_period (year=year,month=month, target_counties=target_counties)
            logger.info(sun + f'{args.yrmonth}: {total}')
            return
        # ---------------------------------------------------
        if args.year:
            total = get_fatalities_for_period (args.year,target_counties)
            logger.info (f'Calendar year {args.year}: {total}')
            return
    # ---------------------------------------------------
    if args.plot:
        # Produce a Bokeh bar plot and show in browser
        fatalities_per_calendar_period_by_year = {} # Could be for a month per year or entire year
        today = arrow.utcnow()

        if args.yrmonth:
            fields = args.yrmonth.split('-')
            month = fields[1]
        else:
            month = None
        for yndx in range(10,0,-1):
            d1 = today.shift (years=-1*yndx)
            total = get_fatalities_for_period(year=d1.year,month=month, target_counties=target_counties)
            fatalities_per_calendar_period_by_year[d1.year] = total

        tag = ''
        if args.county:
            tag = f' For {args.county}'
        if args.yrmonth:
            tag += f' month of {month} only'

        p = figure(title=f"Fatalites {tag}", x_axis_label='Year', y_axis_label='Fatalities',width=800, height=600)
        p.vbar(x=list(fatalities_per_calendar_period_by_year.keys()),
               top=list(fatalities_per_calendar_period_by_year.values()),
               width=0.9)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0

        show(p)


if __name__ == '__main__':
    main()