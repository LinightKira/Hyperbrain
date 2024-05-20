from app_server.db import Base, db


class TableInfo(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键")
    table_name = db.Column(db.String(255), comment="表名")
    table_comment = db.Column(db.String(255), comment="表注释")
    table_columns = db.Column(db.Text, comment="表字段")  # 表字段是一个TableColumn的数组字符串


class TableColumn:
    def __init__(self, column_name, column_comment, column_type):
        self.column_name = column_name
        self.column_comment = column_comment
        self.column_type = column_type


