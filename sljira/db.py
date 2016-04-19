import sqlite3


class KeyValStore(object):
    """
    A simple key value store.
    """
    def __init__(self, db_name="default.db"):

        # establish the connection and initiate cursor
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        # get or create table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS keyval (
                key CHAR(100) PRIMARY KEY,
                value TEXT
            );
            """
        )
        self.connection.commit()

    def get(self, key):
        self.cursor.execute("SELECT value FROM keyval WHERE key=?", (key, ))
        try:
            return self.cursor.fetchone()[0]
        except (IndexError, TypeError):
            return None

    def set(self, key, value):
        existing_val = self.get(key)
        """
        UPDATE table_name
        SET column1 = value1, column2 = value2...., columnN = valueN
        WHERE [condition];
        """
        if existing_val:
            self.cursor.execute(
                "UPDATE keyval SET value=? WHERE key=?", (value, key)
            )
        else:
            self.cursor.execute(
                "INSERT INTO keyval(key, value) VALUES (?, ?)", (key, value)
            )
        self.connection.commit()
        return value
