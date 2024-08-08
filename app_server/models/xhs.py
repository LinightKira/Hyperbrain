from app_server.db import Base, db


# 小红书爬虫内容
class xhsContent(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="自增主键")
    xhs_id = db.Column(db.String(255), nullable=False, unique=False, comment="小红书号")
    xhs_nickname = db.Column(db.String(255), nullable=False, comment="小红书昵称")
    content_title = db.Column(db.String(255), nullable=True, comment="内容标题")
    content_detail = db.Column(db.Text, nullable=True, comment="内容详情")
    content_url = db.Column(db.String(255), nullable=False, unique=True, comment="内容URL")
