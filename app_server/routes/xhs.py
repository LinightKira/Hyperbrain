from flask import request, jsonify, Blueprint

from app_server import db
from app_server.models.xhs import xhsContent

xhs_bp = Blueprint('xhs', __name__)


@xhs_bp.route('/add_xhs_content', methods=['POST'])
def add_xiaohongshu_content():
    data = request.get_json()

    # Check if content_url is provided
    if not data.get('content_url'):
        return jsonify({'error': 'Content URL is required'}), 400

    # Filter xhs_id to remove "小红书号："
    raw_xhs_id = data.get('xhs_id', '')
    filtered_xhs_id = raw_xhs_id.replace('小红书号：', '')

    new_content = xhsContent(
        xhs_id=filtered_xhs_id,
        xhs_nickname=data.get('xhs_nickname'),
        content_title=data.get('content_title'),
        content_detail=data.get('content_detail'),
        content_url=data.get('content_url')
    )

    try:
        new_content.create()
        return jsonify({'message': 'New content added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
