from flask import Flask, flash, render_template, redirect, request, session, url_for
import mysql.connector
import os
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid

app = Flask(__name__,
            template_folder='templates',
            static_folder='src/static',
            static_url_path='/static')

# file path to store user images
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection info. Note that this is not a secure connection.
db_config = {
    'user': 'root',
    'password': '123456789',
    'host': '127.0.0.1',
    'database': 'swiftselldb'
}

# Setting the secret key to a random collection of characters. Tell no-one!
app.secret_key = '2e2f346d432544a7bb0e08738ad38356' 

@app.route('/', methods=['GET'])
def search():
    conn = None
    cursor = None
    categories = []
    search_results = []
    recent_items = []
    total_items_count = 0
    category_names = {}
    try:
        search_query = request.args.get('search_query', '').strip()
        category = request.args.get('category', 'all').strip()
        sort_by = request.args.get('sort_by', None)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT categories_id, category_name FROM categories")
        categories = cursor.fetchall()
        # Fetch categories and create a dictionary with string keys
        category_names = {str(cat['categories_id']): cat['category_name'] for cat in categories}

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
                LIMIT 6
            """)
            recent_items = cursor.fetchall()
            
        # Compute total visible items
        total_items_count = len(search_results) + len(recent_items)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('search_results.html',
                           search_results=search_results,
                           recent_items=recent_items,
                           categories=categories,
                           category_names = category_names,
                           number_of_results_shown=len(search_results),
                           total_results=len(search_results),
                           total_items_count=total_items_count,
                           search_query=search_query,
                           
                           category=category,
                           sort_by=sort_by)

    
# @app.route('/')
# def home():
#     return render_template('home.html')

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Forget any current session user_id
    session.clear()

    if request.method == "POST":
        
        username = request.form['username']
        pwd = request.form['password']

         # Check if username and password are provided
        if not username or not pwd:
            return "Both username and password are required."
        
        # Query database for username
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        # executing query to see if entered user exists
        cursor.execute("SELECT user_id, username, password FROM registered_user WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password_hash = user['password']
            if check_password_hash(stored_password_hash, pwd):
                # creating session variable for curr user's id (used for post item)
                session['user_id'] = user['user_id']
                return redirect(url_for('search'))  # Redirect to the home page
            else:
                return "Invalid password."
        else:
            return "User not found."

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        
        if not username or not password:
            return render_template("signup.html", error="Username and password are required.")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        try:
            # Check if username already exists
            cursor.execute("SELECT * FROM registered_user WHERE username = %s", (username,))
            if cursor.fetchone():
                return render_template("signup.html", error="Username already exists.")

            # Hash the password
            hashed = generate_password_hash(password)

            # Insert the new user
            cursor.execute(
                "INSERT INTO registered_user (username, password, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)",
                (username, hashed, first_name, last_name, email)
            )
            conn.commit()  # Commit to save changes to the database

            return redirect("/login")  # Redirect to login after successful signup
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return render_template("signup.html", error="Failed to register user.")
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template('signup.html')


@app.route("/post", methods=["GET", "POST"])
def post():
    # Check if the user is logged in
    if "user_id" not in session:
        flash("You must be logged in to post an item.")
        return redirect(url_for('login'))

    # Get user ID from session
    user_id = session['user_id']
    print(user_id)
    #check if user wants to post item for sale
    if request.method == 'POST':
        if request.form.get('action') == "item":
            # Grabbing required form info for item
            title = request.form.get('title')
            description = request.form.get('description')
            price = request.form.get('price')
            category_id = request.form.get('category_id')
            photo_path = request.files.get('photo_path')
            # check user entered 
            if not all([title, description, price, category_id, photo_path]):
                flash("All fields are required!")
                return render_template('post.html')
            
            # initializing db cursor
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

           
            try:
                # Process file upload
                pic_filename = secure_filename(photo_path.filename)
                pic_name = f"{uuid.uuid4()}_{pic_filename}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], pic_name)
                photo_path.save(save_path)
                pic_name = save_path

                # Insert item data into database
                cursor.execute("""
                    INSERT INTO items_for_sale (title, description, price, live, seller, category_id, photo_path, thumbnail)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (title, description, price, 0, user_id, category_id, pic_name, pic_name))
                conn.commit()
                flash("Item posted successfully! Waiting for approval.")
            except Exception as e:
                flash(f"An error occurred: {e}")
                return render_template('post.html'), 500
            
                
        elif request.form.get('action') == "service":
            #grab service info from user
            try:
                title = request.form.get('service_title')
                description = request.form.get('service_description')
                price = request.form.get('service_price')
                if not all([title, description, price]):
                    flash("All fields are required!")
                    return render_template('post.html')
                category_id = 4  # Assuming service category ID is fixed
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO items_for_sale (title, description, price, live, seller, category_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (title, description, price, 0, user_id, category_id))
                conn.commit()
                flash("Service posted successfully! Waiting for approval.")
            except Exception as e:
                flash(f"An error occurred: {e}")
                return render_template('post.html'), 500
            
        cursor.close()
        conn.close()
        # Redirect to a different page after successful submission
        return redirect(url_for('post'))

    # Render the post.html template for GET requests
    return render_template('post.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/item/<int:item_id>')
def item_details(item_id):
    # Initialize the database connection and cursor
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Execute a query to fetch details of the specific item using its ID
        cursor.execute("SELECT * FROM items_for_sale WHERE item_id = %s", (item_id,))
        item = cursor.fetchone()
        
        # Check if the item exists
        if item:
            # Render an item detail template if the item is found
            return render_template('item_details.html', item=item)
        else:
            # If no item is found, return a custom error page or a not found message
            return f"Item with ID {item_id} not found.", 404
    except Exception as e:
        # Log exception if something goes wrong
        app.logger.error(f"Error fetching item details: {e}")
        return "An error occurred while fetching item details.", 500
    finally:
        # Ensure that the database cursor and connection are closed properly
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
