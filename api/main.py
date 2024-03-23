import hashlib
import time
from flask import Flask, Response, request
import httpx
from openai import OpenAI, Stream
import pdfplumber
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建 upload 文件夹
import os
if not os.path.exists('upload'):
    os.makedirs('upload')

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    path = Column(String)


# 创建SQLite数据库的连接
engine = create_engine('sqlite:///data.db')

# 创建表
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()


def success_response(data):
    return {
        "ok": True,
        "data": data
    }


def error_response(message):
    return {
        "ok": False,
        "message": message
    }


app = Flask(__name__)
client = OpenAI()

CORS(app)


@app.route("/api/parse")
def hello_world():
    # 通过文件 id 获取文件
    file_id = request.args.get('fileId')
    file = session.query(File).filter(File.id == file_id).first()
    if not file:
        return error_response("文件不存在")

    with pdfplumber.open(file.path) as pdf:
        content = ''
        for pdf_page in pdf.pages:
            raw_text = pdf_page.extract_text()
            if raw_text:
                raw_text_lines = raw_text.splitlines()
                cleaned_raw_text_lines = [
                    line.strip() for line in raw_text_lines if line.strip()]
                cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                content += cleaned_raw_text

    def generate():
        print(cleaned_raw_text)
        prompt = f"将文本的句子进行分割，返回 JSON 格式：{content}"
        stream: Stream = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in stream:
            if chunk is None:
                yield "data: [DONE]\n\n"
                break
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content)
                yield f"data: {chunk.choices[0].delta.content}\n\n"
    return Response(generate(), mimetype="text/event-stream")


@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files['file']
    print(file)
    # 生成 md5 文件名
    filename = hashlib.md5(file.filename.encode()).hexdigest()
    # 如果有直接返回文件 id
    exist_file = session.query(File).filter(File.name == filename).first()

    if not exist_file:
        # 当前文件夹下的 upload 文件夹
        filepath = 'upload/' + filename + '.pdf'
        file.save(filepath)
        exist_file = File(name=filename, path=filepath)
        session.add(exist_file)
        # 提交会话
        session.commit()

    with pdfplumber.open(exist_file.path) as pdf:
        content = ''
        for pdf_page in pdf.pages:
            raw_text = pdf_page.extract_text()
            if raw_text:
                raw_text_lines = raw_text.splitlines()
                cleaned_raw_text_lines = [
                    line.strip() for line in raw_text_lines if line.strip()]
                cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                content += cleaned_raw_text

    # 开始分割句子
    print(cleaned_raw_text)
    prompt = f"将文本按照句子进行分割，以 JSON 的格式输出。下面是句子原文：{content}"
    print(prompt)
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    print(response.choices[0].message.content)

    return success_response(exist_file.id)


if __name__ == "__main__":
    app.run(debug=True)
