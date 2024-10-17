class Database:
    def __init__(self):
        self.tables = {}
        self.current_table = None

    def create_table(self, name):
        self.tables[name] = []
        self.current_table = name

    def insert(self, record):
        if self.current_table is not None:
            self.tables[self.current_table].append(record)

    def select(self):
        return self.tables.get(self.current_table, [])

    def navigate(self, table_name):
        self.current_table = table_name

    def delete(self, index):
        if self.current_table is not None and 0 <= index < len(self.tables[self.current_table]):
            del self.tables[self.current_table][index]