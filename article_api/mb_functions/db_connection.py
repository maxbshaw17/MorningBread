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

    def delete_from_table(self, table: str, days: float = 0, clear: bool = False) -> int:
        if clear: # remove all entries
            try:
                self.mycursor.execute(f"DELETE FROM {table}")
                self.articles_db.commit()
                print(f'deleted {self.mycursor.rowcount} rows from "{table}"')
            except Exception as error:
                self.articles_db.rollback()
                print(f'error deleting from "{table}": {error}')
            finally:
                return self.mycursor.rowcount

        else: # delete entries based on date field
            time_cutoff = datetime.now() - timedelta(days=days)

            insert_sql = f"DELETE FROM {table} WHERE date < '{str(time_cutoff)}'"

            try:
                self.mycursor.execute(insert_sql)
                self.articles_db.commit()
                print(f'deleted {self.mycursor.rowcount} rows from "{table}"')
            except Exception as error:
                self.articles_db.rollback()
                print(f'error deleting from "{table}": {error}')
            finally:
                return self.mycursor.rowcount

    def delete_dupes_from_table(self, table: str, columns: list) -> int:
        columns_string = ", ".join(columns)
        
        insert_sql = f"""delete from `{table}` where id not in
                        ( SELECT * FROM 
                            (select min(id) from `{table}` group by {columns_string}) AS temp_tab
                        );"""
        
        try:
            self.mycursor.execute(insert_sql)
            self.articles_db.commit()
            print(f'deleted {self.mycursor.rowcount} duplicate rows from "{table}"')
        except Exception as error:
            self.articles_db.rollback()
            print(f'error deleting from "{table}": {error}')
        finally:
            return self.mycursor.rowcount

    def join_groups(self):
        insert_sql = """INSERT INTO articles_grouped SELECT headline_groups.*, articles.link, articles.`date`, articles.`source`
        FROM headline_groups 
        JOIN articles ON headline_groups.headline = articles.headline;"""

        try:
            self.mycursor.execute(insert_sql)
            self.articles_db.commit()
        except Exception as error:
            print(f"error joining tables: {error}")
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

    def pull_from_table(self, table: str, columns: list = []) -> pd.DataFrame:
        data = []
        columns_string = ""
        
        if columns: # columns are provided
            columns_string = f"({", ".join(columns)})"
            
        self.mycursor.execute(f"SELECT {columns_string} FROM {table}")

        for row in self.mycursor:
            data.append(row)

        df = pd.DataFrame(
            data, columns=['id', 'group_id', 'headline', 'link', 'date', 'source'])

        return df
