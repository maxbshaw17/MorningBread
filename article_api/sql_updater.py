#imports
from web_scrape.news_scraper import *
import mysql.connector

#create database connection object
articles_db = mysql.connector.connect(
    host = "mysql-2ed0e70f-morningbread.a.aivencloud.com",
    user = "avnadmin",
    password = "AVNS_-1y1cgAxePfkqdPTpji",
    port = 25747,
    database = "morningbread"
)

mycursor = articles_db.cursor()

def insert_articles_db():
    insert_sql = "INSERT INTO articles (headline, link, date, source) VALUES (%s, %s, %s, %s)"

    articles = scrape_all()
    values = []

    for article in articles:
        values.append((article.headline, article.link, article.date, article.source))

    try:
        mycursor.executemany(insert_sql, values)
        articles_db.commit()
    except Exception as error:
        articles_db.rollback()
        print(error)
    finally:
        return mycursor.rowcount
      
def insert_groupings_db(df):
  insert_sql = "INSERT INTO articles_grouped (group_id, headline) VALUES (%s, %s)"
  
  values = []
  
  for index, row in df.iterrows():
    values.append((row['group'], row['sentence']))
    
    
    
  try:
    mycursor.executemany(insert_sql, values)
    articles_db.commit()
  except Exception as error:
    articles_db.rollback()
    print('error')
  finally:
    return mycursor.rowcount
     
def delete_old_db(days):
  time_cutoff = datetime.datetime.now() - timedelta(days = days)
    
  insert_sql = f"DELETE FROM articles WHERE date < '{str(time_cutoff)}'"
    
  try:
    mycursor.execute(insert_sql)
    articles_db.commit()
  except:
    articles_db.rollback()
  finally:
    return mycursor.rowcount

def remove_dupes_db(table, column):
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
    
  except Exception as error:
    articles_db.rollback()
    print(error)
  finally:
    return mycursor.rowcount
  
def delete_all(table):
  insert_sql = f"DELETE FROM {table}"
  
  try:
    mycursor.execute(insert_sql)
    articles_db.commit()
  except:
    articles_db.rollback()
  finally:
    return mycursor.rowcount