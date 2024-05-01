from flask import Flask, jsonify
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
    return "Welcome to MorningBread!"

@app.route('/dynamic_api/articles_api', methods=['GET'])
def get_articles():
    # Query the database for summarized headlines and links

    # PROBLEM BELOW
    c.execute("SELECT summarized_articles.summarized_headline, articles_grouped.link FROM summarized_articles, articles_grouped WHERE summarized_articles.group_id = articles_grouped.group_id")
    # PROBLEM ABOVE
    
    articles = c.fetchall()
    column_names = [column[0] for column in c.description]

    # Convert the articles to a list of dictionaries
    article_list = [dict(zip(column_names, row)) for row in articles]

    return jsonify(article_list)

if __name__ == '__main__':
    app.run(debug=True)
