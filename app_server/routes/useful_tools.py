from datetime import date
from http import HTTPStatus
from flask import jsonify, Blueprint

tools_bp = Blueprint('tools', __name__)


@tools_bp.route('/usefulltools/today_date', methods=['GET'])
def get_today_data():
    try:
        # 返回当前日期
        # 获取当前日期
        today = date.today()
        print("当前日期:", today)

        return jsonify({"code": HTTPStatus.OK, "msg": "success", "data": today})

    except Exception as e:
        print('error', e)
        return jsonify({"code": HTTPStatus.INTERNAL_SERVER_ERROR, "msg": str(e)})
