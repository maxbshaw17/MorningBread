# imports
import mysql.connector
from datetime import timedelta
from datetime import datetime
import pandas as pd


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

    def insert_into_table(self, table: str, dataframe: pd.DataFrame, column_relationships: dict = {}) -> int:
        # initialize column names, value array, column count
        column_names_string = ""
        values = []
        col_count = 0
        
        if column_relationships: # column relationships provided
            column_names_string = ", ".join(column_relationships.values()) # set sql column names
            col_count = len(column_relationships)
            
            # add values in order provided
            for index, row in dataframe.iterrows():
                value_row = []
                
                for key in column_relationships.keys():
                    value_row.append(row[key])
                    
                values.append(value_row)
        
        else: # no relationships provided
            column_names_string = ", ".join(dataframe.columns)# get columns and convert to a string
            col_count = len(dataframe.columns)
            
            # add values in order in the df
            for index, row in dataframe.iterrows():
                values.append(tuple(row))

        # create values placeholder string
        values_placeholder = "%s, " * col_count
        values_placeholder = values_placeholder[:-2]

        # compile the sql command
        insert_sql = f"INSERT INTO {table} ({column_names_string}) VALUES ({values_placeholder})"
        
        # execute sql
        try:
            self.mycursor.executemany(insert_sql, values)
            self.articles_db.commit()
            print(f'inserted {self.mycursor.rowcount} rows to "{table}"')
        except Exception as error:
            self.articles_db.rollback()
            print(f'error inserting into "{table}": {error}')
        finally:
            return self.mycursor.rowcount
        
    def insert_summaries_db(self, summaries):
        insert_sql = "INSERT INTO summarized_articles (group_id, summarized_headline) VALUES (%s, %s)"

        values = []

        for summary in summaries:
            values.append((summary[0], summary[1]))

        try:
            self.mycursor.executemany(insert_sql, values)
            self.articles_db.commit()
        except Exception as error:
            self.articles_db.rollback()
            print(error)
        finally:
            return self.mycursor.rowcount

    def insert_groupings_db(self, df):
        insert_sql = "INSERT INTO headline_groups (group_id, headline) VALUES (%s, %s)"

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

    def join_groups(self):
        insert_sql = """INSERT INTO articles_grouped SELECT headline_groups.*, articles.link, articles.`date`, articles.`source`
        FROM headline_groups 
        JOIN articles ON headline_groups.headline = articles.headline;"""

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

    def get_groups(self):
        data = []
        self.mycursor.execute("SELECT * FROM articles_grouped")

        for x in self.mycursor:
            data.append(x)

        df = pd.DataFrame(
            data, columns=['id', 'group_id', 'headline', 'link', 'date', 'source'])

        return df