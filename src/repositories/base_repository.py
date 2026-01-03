# Base repository providing basic CRUD operations
class BaseRepository:
    def __init__(self, connection):
        """
        connection: a pyodbc connection object
        """
        self.conn = connection

    def execute(self, query, params=None):
        """
        Execute a single query with optional parameters
        """
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            self.conn.rollback()
            raise e

