from flask import Blueprint, Flask, request, render_template, url_for,  Session
from flask_paginate import Pagination, get_page_parameter, get_page_args

# data Extract
ym = [201801, 201802, 201803, 201804, 201805, 201806, 201807, 201808, 201809, 201810, 201811, 201812]
per_month_use_money = []
accountValue = [[20180303,20180201],[20180404,20180901]]
for account in accountValue:

    use_money = account[0]  # 10000
    use_date = account[1]  # 20180909
    for date in ym:  # 201809
        if int(use_date / 100) == date:
            per_month_use_money[date] += use_money
