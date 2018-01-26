from flask import Blueprint, Flask, request, render_template, url_for,  Session
from flask_paginate import Pagination, get_page_parameter, get_page_args

app = Flask(__name__)

@app.route('/')
def dashboard():
    page = int(request.args.get('page', 1))

    File=[]
    for i in range(1, 50):
        file_dict = {"username":str(i), "title":str(i)}
        File.append(file_dict)

    files=File[(page-1)*20:(page-1)*20+20]

    search = False
    q = request.args.get('q')
    if q:
        search = True

    pagination = Pagination(page=page,
                           total=len(File), css_framework='bootstrap4',
                           search=search, per_page=20)

    return render_template('test.html', files=files, pagination=pagination)


if __name__ == '__main__':
    app.run()