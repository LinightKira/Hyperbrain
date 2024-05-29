from flask import Blueprint, request, jsonify
from http import HTTPStatus
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app_server import db

sql_bp = Blueprint('sql', __name__, url_prefix='/sql')


@sql_bp.route('/execute', methods=['POST'])
def execute_sql():
    try:
        sql_statement = request.get_json().get('sql')
        if not sql_statement:
            return jsonify({"code": HTTPStatus.BAD_REQUEST, "msg": "Missing SQL statement"}), HTTPStatus.BAD_REQUEST

        # 获取数据库连接
        conn = db.engine.connect()

        # 执行 SQL 语句
        result = conn.execute(text(sql_statement))

        # 如果是查询语句，获取所有结果并返回
        if result.returns_rows:
            columns = result.keys()  # 获取列名
            rows = result.fetchall()  # 获取所有行
            data = {column: [row[idx] for row in rows] for idx, column in enumerate(columns)}
        else:
            # 如果是非查询语句，返回受影响的行数
            if sql_statement.strip().lower().startswith(('insert', 'update', 'delete')):
                db.session.commit()
                data = {"rows_affected": result.rowcount}
            else:
                data = {"msg": "Non-query SQL executed successfully"}

        # 关闭连接
        conn.close()

        return jsonify({"code": HTTPStatus.OK, "msg": "SQL execution successful", "data": data})
    except SQLAlchemyError as e:
        return jsonify({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
