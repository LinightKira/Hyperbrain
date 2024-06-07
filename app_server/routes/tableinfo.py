import ast
import json
from datetime import datetime
from http import HTTPStatus

from _decimal import Decimal
from flask import request, jsonify, Blueprint
import re

from sqlalchemy import text

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


# 自定义的JSON序列化器，用于处理Decimal和datetime对象
def custom_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


@tableInfo_bp.route('/tableInfo/query/v2', methods=['POST'])
def get_table_columns2():
    request_data = request.data.decode('utf-8')  # 将字节数据解码为字符串
    print('request.data:', request_data, type(request_data))
    request_data = re.sub(r'\b(\w+)\b', r"'\1'", request_data)

    # 数据清洗，过滤多余的引号
    request_data = request_data.replace('\\"', "")
    print('request.data:', request_data, type(request_data))
    table_columns_str = ''  # 表字段详情的字符串
    table_data_demo = ''  # 表数据示例

    try:

        table_names = parse_names_array(request_data)
        # 数据清洗，过滤多余的引号
        table_names = filter_quotes(table_names)

        print('table_names:', table_names, type(table_names))

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

                # 执行SQL查询获取前3条数据
                table_data_temp = get_table_data(table_name)
                # print('table_data_temp:', table_data_temp)
                temp_list = convert_to_dict_of_lists(table_data_temp)
                print('temp_list:', temp_list, type(temp_list))
                table_data_str = json.dumps(temp_list, default=custom_serializer, ensure_ascii=False)
                table_data_demo = table_data_demo + f"TableName--{table_name}:\n{table_data_str}\n"


            else:
                table_columns_str += f"Table '{table_name}' not found.\n"

        print('table_columns_str:', table_columns_str)
        print('table_data_demo:', table_data_demo)

        return jsonify(
            {"code": HTTPStatus.OK, "msg": "success", "data": {"columns": table_columns_str, "rows": table_data_demo}})

    except Exception as e:
        return jsonify({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": str(e)})


def get_table_data(table_name, num=3):
    try:
        # 使用 text() 构造函数创建一个可执行的 SQL 语句对象
        sql_query = text(f"SELECT * FROM {table_name} LIMIT {num}")
        # 获取数据库连接
        conn = db.engine.connect()

        # 执行 SQL 语句
        result = conn.execute(sql_query)

        # 关闭连接
        conn.close()

        rows = [dict(row) for row in result.mappings().all()]
        return rows
    except Exception as e:
        print(f"Error fetching data from {table_name}: {str(e)}")
        return None


# 更改SQL的数据格式
def convert_to_dict_of_lists(data):
    result = {}
    if not data:
        return result

    # 获取所有字段名
    fields = data[0].keys()

    # 初始化每个字段的集合
    for field in fields:
        result[field] = set()

    # 遍历每一行数据，将每个字段的值添加到对应的集合中
    for row in data:
        for field in fields:
            result[field].add(row[field])

    # 将集合转换回列表
    for field in fields:
        result[field] = list(result[field])

    return result


# 过滤掉单引号和双引号
def filter_quotes(table_names):
    filtered_names = []
    for name in table_names:
        filtered_name = re.sub(r"['\"]+", "", name)
        filtered_names.append(filtered_name)
    return filtered_names


def print_string_ends(input_string):
    if len(input_string) < 2:
        print("输入的字符串太短，无法提取开头和结尾部分。")
    else:
        start = input_string[0]
        end = input_string[-1]
        print(f"开头: {start}, 结尾: {end}")


def parse_names_array(input_string):
    print(f"原始输入字符串: {input_string}")

    # 去掉输入字符串两端的双引号
    if input_string.startswith('"') and input_string.endswith('"'):
        input_string = input_string[1:-1]

    # print_string_ends(input_string)
    try:
        if not (input_string.startswith("[") and input_string.endswith("]")):
            raise ValueError("输入的字符串格式不正确")

        names_list = ast.literal_eval(input_string)

        if isinstance(names_list, list):
            return names_list
        else:
            raise ValueError("输入的字符串格式不正确")
    except (ValueError, SyntaxError):
        raise ValueError("输入的字符串格式不正确")
