from flask import Flask, render_template, request
import mysql.connector
import logging

app = Flask(__name__)

# MySQL Configuration
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'dev26052003'
mysql_db = 'skincare_db'

# Function to get a database connection
def get_database_connection():
    return mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_db
    )

# Create table if not exists
def create_survey_data_table():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS survey_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT,
    gender VARCHAR(255),
    allergies VARCHAR(255),
    skin_type VARCHAR(255),
    sun_exposure VARCHAR(255),
    hydration VARCHAR(255),
    products_used INT,
    stress VARCHAR(255),
    sleep INT,
    diet VARCHAR(255),
    exercise VARCHAR(255),
    smoking VARCHAR(255),
    alcohol VARCHAR(255),
    skin_concerns VARCHAR(255),
    preferred_products VARCHAR(255)
);
    """)
    conn.commit()
    cursor.close()
    conn.close()

create_survey_data_table()  # Create the table when the application starts



# Route to render the home.html page
@app.route('/')
def home():
    return render_template('home.html')

# Route to render the project.html page
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

@app.route('/combination_products')
def combination_products():
    return render_template('combination_products.html')

@app.route('/dry_products')
def dry_products():
    return render_template('dry_products.html')

@app.route('/oily_products')
def oily_products():
    return render_template('oily_products.html')

@app.route('/file2')
def file2():
    return render_template('file2.html')


# Route to handle form submission
@app.route("/submit", methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            age = request.form['age']
            gender = request.form['gender']
            allergies = request.form['allergies']
            skin_type = request.form['skinType']
            sun_exposure = request.form['sunExposure']
            hydration = request.form['hydration']
            products_used = request.form['productsUsed']
            stress = request.form['stress']
            sleep_hours = request.form['sleep']
            diet = request.form['diet']
            exercise = request.form['exercise']
            smoking = request.form['smoking']
            alcohol = request.form['alcohol']
            skin_concerns = request.form.getlist('skinConcerns')
            preferred_products = request.form['preferredProducts']

            # Insert data into the database
            conn = get_database_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO survey_data (age, gender, allergies, skin_type, sun_exposure, hydration, 
                                        products_used, stress, sleep_hours, diet, exercise, smoking, 
                                        alcohol, skin_concerns, preferred_products)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (age, gender, allergies, skin_type, sun_exposure, hydration, products_used,
                  stress, sleep_hours, diet, exercise, smoking, alcohol, ','.join(skin_concerns), preferred_products))
            conn.commit()
            cursor.close()
            conn.close()
            if skin_type == "oily":
                return render_template('oily_products.html')
            elif skin_type == "dry":
                return render_template('dry_products.html')
            elif skin_type == "combination":
                return render_template('combination_products.html')
            elif skin_type == "normal":
                return render_template('file2.html')
            else:
                return render_template('project.html')


        app.config['STATIC_URL_PATH'] = '/static'
            # Log success to the console
        app.logger.info("Form submitted successfully")
    except Exception as e:
        # Log error to the console
        app.logger.error("An error occurred while submitting the form: %s", e)

        # Log failure to the console
        app.logger.error("Form submission failed")

        # Return to the project page
        return render_template('project.html')

if __name__ == '__main__':
    # Set logging level and format
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    app.run(debug=True)
