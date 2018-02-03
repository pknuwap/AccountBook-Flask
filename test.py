from flask import Blueprint, Flask, request, render_template, url_for,  Session
from flask_paginate import Pagination, get_page_parameter, get_page_args

d = 20190909
date = str(d)
month = date[4:6]
print(int(month))