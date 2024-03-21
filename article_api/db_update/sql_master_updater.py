import mysql.connector

articles_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread"
)

mycursor = articles_db.cursor()

def remove_dupes_sql(table, column):
  try:
    command = f"""DELETE FROM 
  {table} 
WHERE 
  id IN (
    SELECT 
      id 
    FROM 
      (
        SELECT 
          id, 
          ROW_NUMBER() OVER (
            PARTITION BY {column} 
            ORDER BY 
              {column}
          ) AS row_num 
        FROM 
          {table}
      ) t 
    WHERE 
      row_num > 1
  );"""

    mycursor.execute(command)
    
    articles_db.commit()
    
  except:
    articles_db.rollback()
  
  finally:
    return mycursor.rowcount

rows = remove_dupes_sql("articles", "headline")

print(rows)