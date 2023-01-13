#! /usr/local/bin/python3

import os,sys
import arrow
import random
import datetime
import argparse
from pick import *
from subprocess import *
from setup_logger import *
from iterfzf import *
import pprint

import requests
from requests.exceptions import HTTPError

rip_url = 'https://www.rip.ie/deathnotices.php'
counties = [
'antrim',
'armagh',
'carlow',
'cavan',
'clare',
'cork',
'derry',
'donegal',
'down',
'dublin',
'fermanagh',
'galway',
'kerry',
'kildare',
'kilkenny',
'laois',
'leitrim',
'limerick',
'longford',
'louth',
'mayo',
'meath',
'monaghan',
'offaly',
'roscommon',
'sligo',
'tipperary',
'tyrone',
'waterford',
'westmeath',
'wexford',
'wicklow'

]

six_counties = ['antrim','armagh','down','derry','fermanagh','tyrone']

republic_counties = list (set(counties)-set(six_counties))

def main():
    parser = argparse.ArgumentParser(description='This does cool stuff man!')
    parser.add_argument('--county',help='Results for the given county (name in lowercase)')
    parser.add_argument('--yrmonth',help='Deaths for specified month of year (in YYYY-MMM format (e.g 2021-Jun))')
    parser.add_argument('--year',help='Deaths for specified  year (in YYYY format (e.g 2021))')
    parser.add_argument('--debug', action="store_true",
                        help='Run in debug mode')
    args = parser.parse_args()
    # ---------------------------------------------------
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
    # ----------------------------------
    target_counties = republic_counties
    if args.county:
        target_counties = [args.county]
    # -----------------------------------
    if args.yrmonth:
        fmt1 = 'YYYY-MMM-DD'
        fmt2 = 'YYYY-MM-DD'
        d1 = arrow.get(f'{args.yrmonth}-01',fmt1)
        d2 = d1.ceil('month')

        params['DateFrom'] = f'{d1.format(fmt2)} 00:00:00'
        params['DateTo'] = f'{d2.format(fmt2)} 23:59:59'

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
            # logger.info (f'{county}: {dcount}')
        logger.info(sun + f'{args.yrmonth}: {total}')

        return

    # ---------------------------------------------------
    if args.year:
        params['DateFrom'] = f'{args.year}-01-01  00:00:00'
        params['DateTo'] = f'{args.year}-12-31 23:59:59'

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

        logger.info (f'Calendar year {args.year}: {total}')
        return



if __name__ == '__main__':
    main()