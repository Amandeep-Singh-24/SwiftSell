from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__,
            template_folder='templates',
            static_folder='src/static',
            static_url_path='/static')

# Database connection info. Note that this is not a secure connection.
db_config = {
    'user': 'root',
    'password': '123456789',
    'host': '127.0.0.1',
    'database': 'swiftselldb'
}

@app.route('/search', methods=['GET'])
def search():
    conn = None
    cursor = None
    categories = []
    try:
        search_query = request.args.get('search_query', '')
        category = request.args.get('category', 'all')
        sort_by = request.args.get('sort_by', None)

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch categories
        cursor.execute("SELECT categories_id, category_name FROM categories")
        categories = cursor.fetchall()

        # Construct SQL query for items based on search parameters
        sql_query = "SELECT it.*, cat.category_name FROM items_for_sale it JOIN categories cat ON it.category_id = cat.categories_id WHERE it.live = 1"
        query_params = []
        if search_query:
            sql_query += " AND (it.title LIKE %s OR it.description LIKE %s)"
            query_params.extend(["%" + search_query + "%", "%" + search_query + "%"])
        if category and category != 'all':
            sql_query += " AND cat.categories_id = %s"
            query_params.append(category)
        if sort_by == 'price_asc':
            sql_query += " ORDER BY it.price ASC"
        elif sort_by == 'price_desc':
            sql_query += " ORDER BY it.price DESC"
        elif sort_by == 'name_asc':
            sql_query += " ORDER BY it.title ASC"
        elif sort_by == 'name_desc':
            sql_query += " ORDER BY it.title DESC"



        # Execute query for items
        cursor.execute(sql_query, query_params)
        search_results = cursor.fetchall()

        # Get total number of results
        total_results = len(search_results)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Pass data to template and render HTML
    return render_template('search_results.html',
                           search_results=search_results,
                           categories=categories,  # Pass categories to the template
                           number_of_results_shown=len(search_results),
                           total_results=total_results,
                           search_query=search_query,
                           category=category,
                           sort_by=sort_by)

    
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
