from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home_intro():
    return render_template('intro.html', name="home_intro")

@app.route('/current')
def current():
    return render_template('current.html', name="current")

@app.route('/home')
def home_main():
    return render_template('home.html', name="home_main")

@app.route('/stat')
def stat():
    return render_template('stat.html', name="stat")


if __name__ == '__main__':
    app.run()
