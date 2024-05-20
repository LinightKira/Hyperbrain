import ast
import json
from http import HTTPStatus
from flask import request, jsonify, Blueprint
import re

from app_server import db
from app_server.models.tableinfo import TableInfo, TableColumn

tableInfo_bp = Blueprint('tableInfo', __name__)


@tableInfo_bp.route('/tableInfo', methods=['POST'])
def create_tableInfo():
    try:
        data = request.get_json()

        table_name = data.get('table_name')
        table_comment = data.get('table_comment')
        table_columns = data.get('table_columns')

        # 处理 table_columns 字段
        columns = []
        for column_data in table_columns:
            column = TableColumn(
                column_name=column_data.get('column_name'),
                column_comment=column_data.get('column_comment'),
                column_type=column_data.get('column_type')
            )
            columns.append(column)

        # 将 columns 列表转换为 JSON 字符串
        columns_json = [
            {
                'column_name': column.column_name,
                'column_comment': column.column_comment,
                'column_type': column.column_type
            }
            for column in columns
        ]
        table_columns_json = json.dumps(columns_json)

        table = TableInfo(
            table_name=table_name,
            table_comment=table_comment,
            table_columns=table_columns_json
        )
        table.create()
        return jsonify({"code": HTTPStatus.OK, "msg": "success", "datas": table.to_dict()})

    except Exception as e:
        db.session.rollback()
        return jsonify({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": str(e)})


@tableInfo_bp.route('/tableInfo/all', methods=['GET'])
def get_all_tableInfo():
    try:
        # 查询全部 TableInfo 对象
        table_info = TableInfo.query.with_entities(TableInfo.table_name, TableInfo.table_comment).all()

        # 将每个 TableInfo 对象转换为字典
        table_info_dict = [{"table_name": table_info.table_name, "table_comment": table_info.table_comment} for
                           table_info in table_info]

        return jsonify({"code": HTTPStatus.OK, "msg": "success", "data": table_info_dict})

    except Exception as e:
        print('error', e)
        return jsonify({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": str(e)})


@tableInfo_bp.route('/tableInfo/query', methods=['POST'])
def get_table_columns():
    request_data = request.data.decode('utf-8')  # 将字节数据解码为字符串
    print('request.data:', request_data, type(request_data))
    request_data = re.sub(r'\b(\w+)\b', r"'\1'", request_data)
    try:
        table_names = ast.literal_eval(request_data)
        # 数据清洗，过滤多余的引号
        table_names = filter_quotes(table_names)
        print('table_names:', table_names)
        table_columns_str = ''
        for table_name in table_names:
            table_info = TableInfo.query.filter_by(table_name=table_name).first()
            if table_info:
                table_columns_json = table_info.table_columns
                table_columns = json.loads(table_columns_json)
                table_columns_str += f"TableName---{table_name}:\n"
                for column in table_columns:
                    column_name = column.get('column_name')
                    column_comment = column.get('column_comment')
                    column_type = column.get('column_type')
                    table_columns_str += f"  {column_name} ({column_type}) - {column_comment}\n"
                table_columns_str += "\n"
            else:
                table_columns_str += f"Table '{table_name}' not found.\n"

        print('table_columns_str:', table_columns_str)

        return jsonify({"code": HTTPStatus.OK, "msg": "success", "data": table_columns_str})

    except Exception as e:
        # print('Error:', e)
        # print('AST Node:', ast.dump(ast.parse(request_data)))
        return jsonify({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": str(e)})


# 过滤掉单引号和双引号
def filter_quotes(table_names):
    filtered_names = []
    for name in table_names:
        filtered_name = re.sub(r"['\"]+", "", name)
        filtered_names.append(filtered_name)
    return filtered_names
