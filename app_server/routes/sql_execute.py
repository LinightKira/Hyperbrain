# import asyncio
#
# from flask import Blueprint, request, jsonify
# from http import HTTPStatus
# from sqlalchemy import text
# from sqlalchemy.exc import SQLAlchemyError
#
# from app_agent.roles.dataAnalyst import DataAnalystAssistant, start_data_analyst
# from app_server import db
#
# sql_bp = Blueprint('sql', __name__, url_prefix='/sql')
#
#
# @sql_bp.route('/execute', methods=['POST'])
# def execute_sql():
#     request_data = request.data.decode('utf-8')  # 将字节数据解码为字符串
#     analysis_switch = False
#     # print('request.data:', request_data, type(request_data))
#
#     try:
#
#         sql_statement = request_data
#
#         print('sql:', sql_statement)
#         if not sql_statement:
#             return jsonify({"code": HTTPStatus.BAD_REQUEST, "msg": "Missing SQL statement"}), HTTPStatus.BAD_REQUEST
#
#         # 获取数据库连接
#         conn = db.engine.connect()
#
#         # 执行 SQL 语句
#         result = conn.execute(text(sql_statement))
#
#         # 如果是查询语句，获取所有结果并返回
#         if result.returns_rows:
#             columns = result.keys()  # 获取列名
#             rows = result.fetchall()  # 获取所有行
#
#             if rows:  # 检查是否有数据
#                 data = {column: [row[idx] for row in rows] for idx, column in enumerate(columns)}
#                 if len(rows) > 2:
#                     analysis_switch = True  # 有数据，打开数据分析开关
#             else:
#                 data = {}
#         else:
#             # 如果是非查询语句，返回受影响的行数
#             if sql_statement.strip().lower().startswith(('insert', 'update', 'delete')):
#                 db.session.commit()
#                 data = {"rows_affected": result.rowcount}
#             else:
#                 data = {"msg": "Non-query SQL executed successfully"}
#
#         # 关闭连接
#         conn.close()
#
#         print('data:', data)
#
#         # 运行 数据分析助手
#         if analysis_switch:
#             asyncio.run(start_data_analyst(str(data)))  # 异步执行
#         return jsonify({"code": HTTPStatus.OK, "msg": "SQL execution successful", "data": data})
#     except SQLAlchemyError as e:
#         return jsonify({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
