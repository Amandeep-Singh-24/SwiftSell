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
    search_results = []
    recent_items = []
    try:
        search_query = request.args.get('search_query', '').strip()
        category = request.args.get('category', 'all').strip()
        sort_by = request.args.get('sort_by', None)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT categories_id, category_name FROM categories")
        categories = cursor.fetchall()

        # Sorting options
        sort_options = {
            'price_asc': 'it.price ASC',
            'price_desc': 'it.price DESC',
            'name_asc': 'it.title ASC',
            'name_desc': 'it.title DESC'
        }
        sql_order_by = " ORDER BY it.listed_date DESC"  # Default sort
        if sort_by in sort_options:
            sql_order_by = f" ORDER BY {sort_options[sort_by]}"

        # SQL query for items
        sql_query = """
            SELECT it.*, cat.category_name FROM items_for_sale it 
            JOIN categories cat ON it.category_id = cat.categories_id 
            WHERE it.live = 1
        """
        query_params = []

        if search_query:
            sql_query += " AND (it.title LIKE %s OR it.description LIKE %s)"
            search_term = f"%{search_query}%"
            query_params.extend([search_term, search_term])

        if category != 'all':
            sql_query += " AND cat.categories_id = %s"
            query_params.append(category)

        sql_query += sql_order_by

        cursor.execute(sql_query, query_params)
        search_results = cursor.fetchall()

        # Also apply sorting to recently listed items if no search query is made
        if not search_query and category == 'all':
            cursor.execute("""
                SELECT it.*, cat.category_name 
                FROM items_for_sale it 
                JOIN categories cat ON it.category_id = cat.categories_id 
                WHERE it.live = 1
                """ + sql_order_by + """
                LIMIT 5
            """)
            recent_items = cursor.fetchall()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('search_results.html',
                           search_results=search_results,
                           recent_items=recent_items,
                           categories=categories,
                           number_of_results_shown=len(search_results),
                           total_results=len(search_results),
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
