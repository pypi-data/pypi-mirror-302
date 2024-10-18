import snowflake.connector
import pandas as pd
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from snowflake.sqlalchemy.snowdialect import SnowflakeDialect

class Snowflake:
    def __init__(self, user, password, account='pfa38014.us-east-1', warehouse='analytics_wh', database='fb_data_dev', schema='fb_db', role='ACCOUNTADMIN'):
        self.account = account
        self.user = user
        self.password = password
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.role = role
        self.connection = None
        self.cursor = None
        self.engine = None
        self._connect()

    def _connect(self):
        try:
            self.connection = snowflake.connector.connect(
                account=self.account,
                user=self.user,
                password=self.password,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
                role=self.role
            )
            self.cursor = self.connection.cursor()
            print("Connected to Snowflake successfully!")

            # Set up SQLAlchemy engine
            SnowflakeDialect.supports_statement_cache = False
            self.engine = create_engine(URL(
                account=self.account,
                user=self.user,
                password=self.password,
                database=self.database,
                schema=self.schema,
                warehouse=self.warehouse,
                role=self.role
            ))
        except snowflake.connector.errors.ProgrammingError as e:
            raise ConnectionError(f"Error connecting to Snowflake: {e}")

    def execute_query(self, query):
        if not self.cursor:
            raise ConnectionError("Not connected to Snowflake. Connection may have failed during initialization.")
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except snowflake.connector.errors.ProgrammingError as e:
            raise RuntimeError(f"Error executing query: {e}")

    def read_to_pandas(self, query):
        if not self.cursor:
            raise ConnectionError("Not connected to Snowflake. Connection may have failed during initialization.")
        try:
            self.cursor.execute(query)
            
            # Fetch column names
            column_names = [desc[0] for desc in self.cursor.description]
            
            # Fetch all rows
            rows = self.cursor.fetchall()
            
            # Create DataFrame
            return pd.DataFrame(rows, columns=column_names)
        except snowflake.connector.errors.ProgrammingError as e:
            raise RuntimeError(f"Error executing query: {e}")

    def write_pandas(self, df, table_name, if_exists):
        if not self.engine:
            raise ConnectionError("SQLAlchemy engine not initialized. Connection may have failed during initialization.")

        valid_if_exists = ['append', 'replace', 'fail']
        if if_exists not in valid_if_exists:
            raise ValueError(f"Invalid value for if_exists. Possible values are: {', '.join(valid_if_exists)}")

        try:
            df.to_sql(name=table_name, con=self.engine, if_exists=if_exists, index=False, method='multi')
            print(f"Successfully wrote {len(df)} rows to {table_name}.")
        except Exception as e:
            raise RuntimeError(f"Error writing DataFrame to Snowflake: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        print("All connections closed.")