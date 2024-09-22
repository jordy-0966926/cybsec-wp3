class Queries:
    def insert_in_table(table_name, columns):
        # use the keys of the dictionary to create the columns
        column_names = ', '.join(columns)
        # for each column, create a placeholder
        placeholders = ', '.join(['?' for _ in columns])
        qry = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        return qry

    @staticmethod
    def get_count(table):
        qry = f"SELECT COUNT(*) FROM {table}"
        return qry
