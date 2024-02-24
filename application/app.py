from flask import Flask, render_template

app = Flask(__name__,
            template_folder='templates',
            static_folder='src/static',
            static_url_path='/static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/amandeepsingh')
def about():
    return render_template('about_amandeep.html')

# @app.route('/about/aymanearfaoui')
# def about():
#     return render_template('about_aymanearfaoui.html')

# @app.route('/about/alexisalvarez')
# def about():
#     return render_template('about_alexisalvarez.html')

# @app.route('/about/davedaly')
# def about():
#     return render_template('about_davedaly.html')

# @app.route('/about/markusreyer')
# def about():
#     return render_template('about_markusreyer.html')

if __name__ == '__main__':
    app.run(debug=True)
