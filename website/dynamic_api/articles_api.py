from flask import Flask, render_template
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask application

# Connect to the MySQL database using environment variables
articles_db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)

c = articles_db.cursor()

@app.route('/')
def index():
    # Query the database for summarized headlines, links, and magnitude (ordered by magnitude descending)
    articles = []
    c.execute("SELECT summarized_articles.summarized_headline summarized_articles.magnitude")
    for article in c:
        articles.append({'headline' : article[0], 'magnitude' : article[1]})
    

    return render_template('index.html', articles = articles)

if __name__ == '__main__':
    app.run(debug=True)
