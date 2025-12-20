import duckdb

class DuckDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        self.con = duckdb.connect("db/clima.duckdb")

    def execute(self, query: str, params=None):
        if params:
            return self.con.execute(query, params)
        return self.con.execute(query)

    def fetchdf(self, query: str, params=None):
        return self.execute(query, params).fetchdf()

    def fetchall(self, query: str, params=None):
        return self.execute(query, params).fetchall()

    def close(self):
        self.con.close()

