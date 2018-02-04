# 보안 및 기타 함수를 모아둔 모듈

def check_password(s,k):
    if k==0: # email
        a = "!#$%^&*()'-,/\+=~"
    else: # password
        a = "!#$%^&*()'-.@,/\+=~_&₩~"

    for i in a:
        for j in s:
            if i == j:
                return False
    return True


def check_null(s):
    if s == "":
        return False
    return True


def check_month(date,input_month):
    date = str(date)
    month = date[4:6]
    if input_month == int(month):
        return True
    return False

# date : 20190128, input_year : 2018
def check_year(date, input_year):
    date = str(date)
    year = date[0:4]
    if str(input_year) == str(year):
        return True
    return False


def parse_month(date):
    date = str(date)
    month = int(date[4:6])
    return month
