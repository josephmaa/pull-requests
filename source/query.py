from typing import Optional
from source.keys import user, passwd, database
import MySQLdb


class Database:
    DATABASE_NAMES = ["sansa"]

    def __init__(self, name: Optional[str]):
        # Currently only have the sansa database to connect to.
        self._databases_to_host = {"sansa": "sansa.cs.uoregon.edu"}
        self._database_name = name
        self._database: Optional[any] = None
        assert (
            name in self._databases_to_host
        ), f"The current database name: {name} has not yet been implemented."
        # Connect to the database.
        self._database = MySQLdb.connect(
            host=self._databases_to_host[name],
            port=3331,
            user=user,
            passwd=passwd,
            database=database,
        )
        self._cursor = self._database.cursor()

    def get_available_databases() -> list[str]:
        return Database.DATABASE_NAMES

    def get_database(self):
        return self._database

    def get_cursor(self):
        return self._cursor

    def execute_query(self, query: "Query") -> str:
        """
        Gets a query result string from the database. Returns and updates the query string result.
        """
        self._cursor.execute(query.get_query_string())
        rows = self._cursor.fetchall()
        self.query_result = rows
        return self.query_result

    def get_schema(self, table: str) -> list[tuple[any]]:
        """
        Gets the schema from said table.
        """
        query = f"DESCRIBE {table}"
        self._cursor.execute(query)
        rows = self._cursor.fetchall()
        return rows


class Query:
    def __init__(self, query_string: Optional[str] = None):
        """
        Query object for the sansa database.
        """
        # Initialize the database object.
        # TODO: Change hardcoded object.
        self._database = Database(name="sansa")
        self._query_string: str = query_string
        self.query_result: Optional[list[tuple[any]]] = None

    def get_query_string(self) -> str:
        return self._query_string


def execute_query(database: Database, query: Query):
    return database.get_cursor().execute(query)
