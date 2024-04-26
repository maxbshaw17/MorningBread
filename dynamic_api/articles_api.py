from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask application

# Connect to the MySQL database
articles_db = mysql.connector.connect(
    host="mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user="avnadmin",
    password="AVNS_-1y1cgAxePfkqdPTpji",
    port=25747,
    database="morningbread",
)
c = articles_db.cursor()

@app.route('/')
def index():
    return "Welcome to MorningBread!"

@app.route('/dynamic_api/articles_api', methods=['GET'])
def get_articles():
    # Query the database for article headlines
    c.execute("SELECT headline FROM articles")
    articles = c.fetchall()
    column_names = [column[0] for column in c.description]

    # Convert the articles to a list of dictionaries
    article_list = [dict(zip(column_names, row)) for row in articles]

    return jsonify(article_list)

if __name__ == '__main__':
    app.run(debug=True)