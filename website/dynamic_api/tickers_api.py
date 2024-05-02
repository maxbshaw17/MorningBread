from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database (Not yet created)
tickers_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread"
)

c = tickers_db.cursor()

@app.route('/dynamic_api/tickers_api', methods=['GET'])
def get_tickers():
    # Query the database for the ticker's symbol, name, change, and percent change
    c.execute("SELECT symbol, name, change, percent_change FROM tickers")
    tickers = c.fetchall()

    # Convert the tickers to a list of dictionaries
    tickers_list = [{'headline': row[0], 'summary': row[1]} for row in tickers]

    return jsonify(tickers_list)

if __name__ == '__main__':
    app.run(debug=True)