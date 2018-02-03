from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from flask_paginate import Pagination
from datetime import datetime
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import sec # 보안/기타 함수모음

mysql = MySQL()
app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'dlxorud7202'
app.config['MYSQL_DATABASE_DB'] = 'accountBook'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# 추후 설정해야함
app.secret_key = '???'

# 홈화면
@app.route('/')
def home_intro():
    return validateLogin()

# 회비납부 화면
@app.route('/current')
def current():
    try:
        if session.get('user'):
            return render_template('current.html',userName=session.get('name'))
        else:
            return render_template('error.html', error="회비납부 현황을 볼 권한이 없습니다. 로그인 해주세요")
    except Exception as e:
        return render_template('error.html', error=str(e))

# 장부화면
@app.route('/home')
def home_main():
    try:
        if session.get('user'):

            con = mysql.connect()
            cursor = con.cursor()

            # 정렬
            sort = request.args.get('sort')
            if sort =="muchmoney":
                cursor.callproc('sp_muchUseMoney')
            elif sort == "oldday":
                cursor.callproc('sp_oldDay')
            elif sort=="lastday":
                cursor.callproc('sp_lastDay')
            else:
                cursor.callproc('sp_GetAccountBookAll')

            search_option = request.args.get('inputSearch')
            search_content = request.args.get('inputSearchContent')

            if search_option == "account_use_user":
                cursor.callproc('sp_search', (0, search_content))
            elif search_option == "account_write_user":
                cursor.callproc('sp_search', (1, search_content))
            elif search_option == "account_use_description":
                cursor.callproc('sp_search', (2, search_content))
            elif search_option == "account_use_date":
                cursor.callproc('sp_search', (3, search_content))
            elif search_option == "account_write_date":
                cursor.callproc('sp_search', (4, search_content))

            account_book = cursor.fetchall()
            account_list = []
            for account in account_book:
                account_dict = {
                    'account_id': account[0],
                    'account_use_user': account[1],
                    'account_use_description': account[2],
                    'account_use_money': account[3],
                    'account_use_date': account[4],
                    'account_write_date': account[5],
                    'account_write_user': account[6],
                }
                account_list.append(account_dict)

            # page navibar
            page = int(request.args.get('page', 1))

            search = False
            q = request.args.get('q')
            if q:
                search = True

            show_account_list = account_list[(page - 1) * 10:(page - 1) * 10 + 10]

            pagination = Pagination(page=page,
                                    total=len(account_list), css_framework='bootstrap4',
                                    search=search, per_page=10,alignment="center")

            return render_template('home.html', show_account_list=show_account_list, pagination=pagination,
                                   userName=session.get('name'))
        else:
            return render_template('error.html', error="장부를 볼 권한이 없습니다. 로그인 해주세요")
    except Exception as e:
        return render_template('error.html', error=str(e))


# 장부추가 아직 수정해야함, 예외처리 필요
@app.route('/addAccount', methods=['POST'])
def addAcount():
    try:
         if session.get('user'):

            _use_name = request.form['use_name']
            _use_description = str(request.form['use_d']).replace("'","").replace("-","")
            _use_money = request.form['use_money']
            _use_date = request.form['use_date']
            _write_name = session.get('name')
            _write_date = int(datetime.today().strftime("%Y%m%d"))
            _use_option = int(request.form['use_option']) # 지출 (0), 수입(1), 회비(2)

            # 특수문자가 포함되어져 있는가 확인 bug fix
            if (sec.check_password(_use_name, 1) or
                sec.check_password(_use_money, 1) or
                sec.check_password(_use_date, 1)) is False:
                return render_template('error.html', error='특수문자 포함 금지')

            _use_money = int(_use_money)
            _use_date = int(_use_date)

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('sp_addAccount', (_use_name, _use_description, _use_money, _use_date, _write_date, _write_name, _use_option))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/home')
            else:
                return render_template('error.html', error='An error occurred!')

    except Exception as e:
        print(str(e))
        return render_template('error.html', error=str(e))


# 로그인
@app.route('/intro', methods=['POST','GET'])
def validateLogin():
    if request.method == 'POST':
        try:
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']

            # security
            if sec.check_password(_password, 1) == False or sec.check_password(_email,0) == False:
                return render_template('intro.html', loginError='특수문자를 제외해주세요.')
            if sec.check_null(_email) == False or sec.check_null(_password) == False:
                return render_template('intro.html', loginError='이메일과 비밀번호를 입력해주세요.')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_validateLogin',(_email,))
            data = cursor.fetchall()

            if len(data) > 0:
                if check_password_hash(str(data[0][1]), _password): # user password compared
                    session['user'] = data[0][0] # user email
                    session['name'] = data[0][2] # user name
                    return render_template('intro.html', userName=str(data[0][2]))
                else:
                    return render_template('intro.html', loginError='잘못된 Email이거나 잘못된 Password 입니다')
            else:
                return render_template('intro.html', loginError='잘못된 Email이거나 잘못된 Password 입니다')

        except Exception as e:
            return render_template('error.html', error=str(e))

    else:
        if session.get('user'):
            return render_template('intro.html', userName=str(session['name']))
        else:
            return render_template('intro.html')


# 회원가입
@app.route('/joinIn', methods=['POST', 'GET'])
def joinIn():
    if request.method == 'POST':
        try:
            _email = request.form['inputEmail']
            _password = request.form['inputPassword'] # 특수문자 허용 x
            _name = request.form['inputName']
            _gender = int(request.form['inputGender']) # man=0, woman=1
            _grade = int(0) # default, 관리자=1

            if _email and _password and _name:
                conn = mysql.connect()
                cursor = conn.cursor()
                _hashed_password = generate_password_hash(_password)
                cursor.callproc('sp_createUser', (_email, _hashed_password, _name, _gender, _grade))
                data = cursor.fetchall()

                if len(data) is 0:
                    conn.commit()
                    return render_template('joinSuccess.html',join=_name + " 님의 아이디(이메일)은 '" +  _email + "' 입니다.")
                else:
                    return render_template('error.html',error=str(data[0]))
            else:
                return render_template('join.html',error="모든 항목을 다 채워주세요.")

        except Exception as e:
            return render_template('error.html', error=str(e))

    else:
        if session.get('user'):
            return render_template('error.html', error="로그아웃 후 가입을 시도해주세요.")
        else:
            return render_template('join.html', name="join")


# 통계 화면
@app.route('/stat')
def stat():
    try:
        if session.get('user'):

            conn = mysql.connect()
            cursor = conn.cursor()
            current_year = int(datetime.today().strftime("%Y"))

            input_year = request.args.get('inputYear')
            if input_year is None:
                input_year = current_year
            else:
                input_year = int(input_year)
            # set value for chart
            per_month_use_money = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 매달 지출
            per_month_get_money = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 매달 수입
            per_month_use_frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            per_month_write_frequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 장부작성 빈도
            per_month_budget = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 매달 남은 예산
            month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] # 달

            cursor.callproc('sp_search_stat', (input_year,))
            stat_list = cursor.fetchall()

            for stat_value in stat_list:

                account_use_money = int(stat_value[3])
                account_use_date = int(stat_value[4])
                account_write_date = int(stat_value[5])
                account_use_option = int(stat_value[7])

                for month in month_list:
                    # 사용일 기준으로 빈도/사용금액 계산
                    if sec.check_month(account_use_date, month):
                        if account_use_option == 0: # 지출
                            per_month_use_money[month-1] += account_use_money # 달마다 돈을 얼마나 썼는가
                            per_month_use_frequency[month-1] += 1 # 매달마다 몇번 돈을 썼는가
                        else: # 수입 (회비 + 수입)
                            per_month_get_money[month-1] += account_use_money

                    # 장부 작성빈도
                    if sec.check_month(account_write_date, month):
                        per_month_write_frequency[month-1] += 1 # 매달 장부를 몇번 썼는가
                m = 0
                for get_money, use_money in zip(per_month_get_money, per_month_use_money):
                    per_month_budget[m] = get_money - use_money
                    m = m+1


            return render_template('stat.html',
                                   currentYear=current_year,
                                   showYear=input_year,
                                   budget=per_month_budget,
                                   getMoneyList = per_month_get_money,
                                   useMoneyList = per_month_use_money,
                                   Write_Frequency_Values = per_month_write_frequency,
                                   Use_Frequency_Values= per_month_use_frequency,
                                   userName=str(session.get('name')))
        else:
            return render_template('error.html', error="장부통계를 볼 권한이 없습니다. 로그인 해주세요")
    except Exception as e:
        return render_template('error.html', error=str(e))


# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


# 에러처리,
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error="404 페이지를 찾을 수 없습니다")

# 프로그램 실행
if __name__ == '__main__':
    app.run()
