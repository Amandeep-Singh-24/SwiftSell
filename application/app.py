from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__,
            template_folder='templates',
            static_folder='src/static',
            static_url_path='/static')

# Database connection info. Note that this is not a secure connection.
db_config = {
    'user': 'ubuntu',
    'password': 'Aman2423!',
    'host': '127.0.0.1',
    'database': 'swiftselldb'
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/amandeepsingh')
def about_amandeepsingh():
    return render_template('about_amandeep.html')

@app.route('/about/aymanearfaoui')
def about_aymanearfaoui():
    return render_template('about_aymanearfaoui.html')

@app.route('/about/alexisalvarez')
def about_alexisalvarez():
    return render_template('about_alexisalvarez.html')

@app.route('/about/davedaly')
def about_davedaly():
    return render_template('about_davedaly.html')

@app.route('/about/markusreyer')
def about_markusreyer():
    return render_template('about_markusreyer.html')

if __name__ == '__main__':
    app.run(debug=True)
