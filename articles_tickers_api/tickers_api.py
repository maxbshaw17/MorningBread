from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the SQL database (Not yet created)
conn = sqlite3.connect('tickers.db')
c = conn.cursor()

@app.route('/articles_tickers_api/tickers_api', methods=['GET'])
def get_tickers():
    # Query the database for the ticker's symbol, name, change, and percent change
    c.execute("SELECT symbol, name, change, percent_change FROM tickers")
    tickers = c.fetchall()

    # Convert the tickers to a list of dictionaries
    tickers_list = [{'headline': row[0], 'summary': row[1]} for row in tickers]

    return jsonify(tickers_list)

if __name__ == '__main__':
    app.run(debug=True)