# imports
import mysql.connector
from datetime import timedelta
from datetime import datetime
import pandas as pd


class DB_Connection:

    def __init__(self, host: str, user: str, password: str, port: int, database: str) -> None:
        self.articles_db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )

        self.mycursor = self.articles_db.cursor()

    def get_row_count(self, table: str) -> int:
        """Gets the total row count of the target table\n
        table: target table in SQL database"""
        
        insert_sql = f"SELECT COUNT(*) AS row_count FROM {table};"
        try:
            self.mycursor.execute(insert_sql)
            
        except Exception as error:
            print(f"error grabbing row count from {table}: {error}")
        
        return self.mycursor.fetchone()[0]
        
    def insert_into_table(self, table: str, dataframe: pd.DataFrame, column_relationships: dict = {}) -> int:
        """Inserts a dataframe into an SQL table\n
        table: target table in SQL database\n
        dataframe: data to insert\n
        column_relationships: dictionary of dataframe and SQL column relationships\n
        \t{dataframe column : sql column}"""
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
            print(f'inserted {self.mycursor.rowcount} rows to "{table}", {self.get_row_count(table)} total rows')
        except Exception as error:
            self.articles_db.rollback()
            print(f'error inserting into "{table}": {error}')
        finally:
            return self.mycursor.rowcount

    def delete_from_table(self, table: str, days: float = 0, clear: bool = False) -> int:
        """Deletes rows from the target table. Deletes based on the date column, or everything is deleted\n
        table: target table\n
        days: how many days in the past to keep\n
        \tFor example, days = 2 keeps rows where the date column is within the last 2 days\n
        clear: if true, deletes all rows from the table, ignoring any other inputs"""
        if clear: # remove all entries
            try:
                self.mycursor.execute(f"DELETE FROM {table}")
                self.articles_db.commit()
                print(f'deleted all ({self.mycursor.rowcount}) rows from "{table}"')
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
                print(f'deleted {self.mycursor.rowcount} rows older than {days} days from "{table}", {self.get_row_count(table)} total rows')
            except Exception as error:
                self.articles_db.rollback()
                print(f'error deleting from "{table}": {error}')
            finally:
                return self.mycursor.rowcount

    def delete_dupes_from_table(self, table: str, columns: list) -> int:
        columns_string = ", ".join(columns)
        
        insert_sql = f"""delete from `{table}` where id not in
                        ( SELECT * FROM 
                            (SELECT MIN(id) FROM `{table}` GROUP BY {columns_string}) AS temp_tab
                        );"""
        
        try:
            self.mycursor.execute(insert_sql)
            self.articles_db.commit()
            print(f'deleted {self.mycursor.rowcount} duplicate rows from "{table}", {self.get_row_count(table)} total rows')
        except Exception as error:
            self.articles_db.rollback()
            print(f'error deleting duplicates from "{table}": {error}')
        finally:
            return self.mycursor.rowcount

    def join_groups(self):
        insert_sql = """
        INSERT INTO articles_grouped (group_id, headline, link, date, source)
        SELECT headline_groups.group_id, articles.headline, articles.link, articles.date, articles.source
            FROM (SELECT articles.*, row_number() OVER (ORDER BY id) AS seqnum
                FROM articles
                ) articles JOIN
                (SELECT headline_groups.*, row_number() OVER (ORDER BY id) AS seqnum
                FROM headline_groups
                ) headline_groups
                ON articles.seqnum = headline_groups.seqnum;"""

        try:
            self.mycursor.execute(insert_sql)
            self.articles_db.commit()
            print(f'inserted {self.mycursor.rowcount} rows to "articles_grouped", {self.get_row_count("articles_grouped")} total rows')
        except Exception as error:
            print(f"error joining tables: {error}")
            self.articles_db.rollback()
        finally:
            return self.mycursor.rowcount

    def read_table(self, table: str, column_relationships: dict = {}) -> pd.DataFrame:
        """Reads from target table and creates a same sized dataframe\n
        table: target table\n
        column_relationships: dictionary of dataframe and SQL column relationships\n
        \t{dataframe column : sql column}"""
        data = []
        sql_columns_string = ""
        df_columns_list = []
        
        if column_relationships: # columns are provided
            sql_columns_string = f'{", ".join(column_relationships.values())}'
            df_columns_list = column_relationships.keys()
        else: # no columns provided, grabs all
            sql_columns_string = '*'
            
            try: # tries to grab all column names
                self.mycursor.execute(f"""SELECT COLUMN_NAME
                                      FROM INFORMATION_SCHEMA.COLUMNS
                                      WHERE TABLE_NAME='{table}'
                                      ORDER BY ORDINAL_POSITION ASC""")
                for column in self.mycursor: # appends columns from returned list
                    df_columns_list.append(column[0]) # for some reason, columns are read in as tuples
            except Exception as error:
                print(f'error retrieveing column names from "{table}": {error}')
        
        try:
            self.mycursor.execute(f"SELECT {sql_columns_string} FROM {table}")
        except Exception as error:
            print(f'error retrieving data from "{table}": {error}')
        
        for row in self.mycursor: # appends rows into data array
            data.append(row)

        df = pd.DataFrame( # converts array into dataframe
            data, columns = df_columns_list)

        return df
