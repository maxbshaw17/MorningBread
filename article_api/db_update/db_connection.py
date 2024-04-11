# imports
import mysql.connector
from datetime import timedelta
from datetime import datetime

class DB_Connection:
    
    def __init__(self, host, user, password, port, database):
        self.articles_db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        
        self.mycursor = self.articles_db.cursor()
        

    def insert_articles_db(self, articles):
        insert_sql = "INSERT INTO articles (headline, link, date, source) VALUES (%s, %s, %s, %s)"

        values = []

        for article in articles:
            values.append((article.headline, article.link,
                        article.date, article.source))

        try:
            self.mycursor.executemany(insert_sql, values)
            self.articles_db.commit()
        except Exception as error:
            self.articles_db.rollback()
            print(error)
        finally:
            return self.mycursor.rowcount


    def insert_groupings_db(self, df):
        insert_sql = "INSERT INTO articles_grouped (group_id, headline) VALUES (%s, %s)"

        values = []

        for index, row in df.iterrows():
            values.append((row['group'], row['sentence']))

        try:
            self.mycursor.executemany(insert_sql, values)
            self.articles_db.commit()
        except Exception as error:
            self.articles_db.rollback()
            print('error')
        finally:
            return self.mycursor.rowcount


    def delete_old_db(self, days):
        time_cutoff = datetime.now() - timedelta(days=days)

        insert_sql = f"DELETE FROM articles WHERE date < '{str(time_cutoff)}'"

        try:
            self.mycursor.execute(insert_sql)
            self.articles_db.commit()
        except:
            self.articles_db.rollback()
        finally:
            return self.mycursor.rowcount


    def remove_dupes_db(self, table, column):
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

            self.mycursor.execute(command)

            self.articles_db.commit()

        except Exception as error:
            self.articles_db.rollback()
            print(error)
        finally:
            return self.mycursor.rowcount


    def delete_all(self, table):
        insert_sql = f"DELETE FROM {table}"

        try:
            self.mycursor.execute(insert_sql)
            self.articles_db.commit()
        except:
            self.articles_db.rollback()
        finally:
            return self.mycursor.rowcount


    def get_all_headlines(self):
        headlines = []
        self.mycursor.execute("SELECT headline FROM articles")
        for x in self.mycursor:
            headlines.append(x[0])

        return headlines


    def execute_sql(self, command_string):
        return_data = []
        self.mycursor.execute(command_string)
        for line in self.mycursor:
            return_data.append(line)

        return return_data
