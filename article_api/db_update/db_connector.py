import mysql.connector

articles_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread"
)

mycursor = articles_db.cursor()

def get_all_headlines():
    headlines = []
    mycursor.execute("SELECT headline FROM articles")
    for x in mycursor:
        headlines.append(x)
    
    return headlines