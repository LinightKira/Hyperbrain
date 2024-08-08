import json
import re
import time

import requests
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

# Flask app and database configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pwd@localhost/media_crawler'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Enable CORS
CORS(app)


# Database models
class XHSNoteComment(db.Model):
    __tablename__ = 'xhs_note_comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(64))
    avatar = db.Column(db.String(255))
    ip_location = db.Column(db.String(255))
    add_ts = db.Column(db.BigInteger, nullable=False)
    last_modify_ts = db.Column(db.BigInteger, nullable=False)
    comment_id = db.Column(db.String(64), nullable=False)
    create_time = db.Column(db.BigInteger, nullable=False)
    note_id = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sub_comment_count = db.Column(db.Integer, nullable=False)
    pictures = db.Column(db.String(512))
    tagged = db.Column(db.Boolean, default=False, nullable=False)  # New field


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255), unique=True, nullable=False)


class XHSNoteCommentTag(db.Model):
    __tablename__ = 'xhs_note_comment_tag'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('xhs_note_comment.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    comment = db.relationship('XHSNoteComment', backref=db.backref('comment_tags', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('tag_comments', lazy=True))


# Function to call coze API and get tags
def call_coze_api(content):
    url = "https://api.coze.cn/open_api/v2/chat"
    headers = {
        "Authorization": "Bearer pat_**********************************",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Host": "api.coze.cn",
        "Connection": "keep-alive"
    }
    payload = {
        "conversation_id": "",
        "bot_id": "*******************",
        "user": "112233",
        "query": content,
        "stream": False
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        if data.get('code') == 0:
            return parse_content(data['messages'][0]['content'])
        else:
            raise Exception(f"Error: {data.get('msg')}")
    else:
        response.raise_for_status()


def call_dify_api(content):
    print('start dify api')
    url = "http://localhost/v1/completion-messages"
    headers = {
        "Authorization": "Bearer app-********************",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {"query": content},
        "response_mode": "blocking",
        "user": "abc-123"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        # parse_content(data['answer'][0]['content'])
        return parse_content(data['answer'])

    else:
        response.raise_for_status()


# Function to parse content and extract tags
def parse_content(content):
    print('content:', content)
    pattern = re.compile(r"\[(.*?)\]")
    match = pattern.search(content)
    if match:
        try:
            tags_str = match.group(1)  # 获取方括号内的内容
            tags = [tag.strip() for tag in tags_str.split(',')]  # 用逗号分割并去除空白
            return tags
        except Exception:
            pass
    return ["非工厂"]


# Utility function to get or create a tag
def get_or_create_tag(tag_name):
    # 清洗 tag_name
    tag_name = clean_tag_name(tag_name)
    tag = Tag.query.filter_by(tag=tag_name).first()
    if not tag:
        try:
            tag = Tag(tag=tag_name)
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            tag = Tag.query.filter_by(tag=tag_name).first()
    return tag


def clean_tag_name(tag_name):
    # 使用正则表达式去除上下引号，包括全角和半角
    cleaned_tag_name = re.sub(r"[\"\'“”‘’]", "", tag_name)
    return cleaned_tag_name


# Batch tagging function placeholder
def batch_tag_comments(comments):
    for comment in comments:
        print(f"Tagging comment id: {comment.id}, content: {comment.content}")
        content_text = comment.content

        if len(content_text) > 0:
            # Call external API to get tags
            # tags = call_coze_api(content_text)
            tags = call_dify_api(content_text)

            # Store tags and relationships
            for tag_name in tags:
                tag = get_or_create_tag(tag_name)
                comment_tag = XHSNoteCommentTag(comment_id=comment.id, tag_id=tag.id)
                db.session.add(comment_tag)

        # Mark comment as tagged
        comment.tagged = True
        # 接口QPS有限制，需要延迟处理
        time.sleep(0.5)


# API route to process content and generate tags
@app.route('/xhs/process', methods=['POST'])
def process_content():
    print('Processing content...')
    data = request.json
    batch_size = data.get('batch_size', 10)  # Default to 10 if not provided

    print(f"Batch size: {batch_size}")
    # Fetch untagged comments
    untagged_comments = XHSNoteComment.query.filter(
        or_(XHSNoteComment.tagged == False, XHSNoteComment.tagged.is_(None))
    ).limit(batch_size).all()

    if not untagged_comments:
        return jsonify({"message": "No untagged comments found"}), 404
    # 给未打标的评论进行打标
    batch_tag_comments(untagged_comments)
    db.session.commit()

    return jsonify({"message": f"{len(untagged_comments)} comments processed and tagged"}), 200


# API route to get paginated comments with tags
@app.route('/api/comments', methods=['GET'])
def get_comments():
    page = request.args.get('page', 1, type=int)
    per_page = 50

    pagination = XHSNoteComment.query.paginate(page=page, per_page=per_page, error_out=False)
    comments = pagination.items

    result = []
    for comment in comments:
        tags = [ct.tag.tag for ct in comment.comment_tags]
        result.append({
            'id': comment.id,
            'user_id': comment.user_id,
            'nickname': comment.nickname,
            'avatar': comment.avatar,
            'ip_location': comment.ip_location,
            'add_ts': comment.add_ts,
            'last_modify_ts': comment.last_modify_ts,
            'comment_id': comment.comment_id,
            'create_time': comment.create_time,
            'note_id': comment.note_id,
            'content': comment.content,
            'sub_comment_count': comment.sub_comment_count,
            'pictures': comment.pictures,
            'tags': tags
        })

    return jsonify({
        'comments': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'next_page': pagination.next_num,
        'prev_page': pagination.prev_num
    })


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

    # 以下为测试代码
    # content_text = '赠品，礼品，促销品，源头厂家发货，百种商品'
    # # print('output:', call_coze_api(content_text))
    # # Call external API to get tags
    # # tags = call_coze_api(content_text)
    # # with app.app_context():
    # #     # Store tags and relationships
    # #     for tag_name in tags:
    # #         tag = get_or_create_tag(tag_name)
    # #
    #
    # tags = call_dify_api(content_text)
    # print('output:', tags)
