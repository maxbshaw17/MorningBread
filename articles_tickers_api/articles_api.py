from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database (Not yet created)
articles_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread",
)

c = articles_db.cursor()

@app.route('/articles_tickers_api/articles_api', methods=['GET'])
def get_articles():
    # Query the database for article headlines and summaries
    c.execute("SELECT headline, summary FROM articles")
    articles = c.fetchall()

    # Convert the articles to a list of dictionaries
    article_list = [{'headline': row[0], 'summary': row[1]} for row in articles]

    return jsonify(article_list)

if __name__ == '__main__':
    app.run(debug=True)
