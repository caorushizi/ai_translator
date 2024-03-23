import time
from flask import Flask, Response
import httpx
from openai import OpenAI, Stream
import pdfplumber
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

with pdfplumber.open("/home/caorushizi/Workspace/Documents/test.pdf") as pdf:
    for pdf_page in pdf.pages:

        # Store the original text content
        raw_text = pdf_page.extract_text()
        tables = pdf_page.extract_tables()

        # Remove each cell's content from the original text
        for table_data in tables:
            for row in table_data:
                for cell in row:
                    raw_text = raw_text.replace(cell, "", 1)

        # Handling text
        if raw_text:
            # Remove empty lines and leading/trailing whitespaces
            raw_text_lines = raw_text.splitlines()
            cleaned_raw_text_lines = [
                line.strip() for line in raw_text_lines if line.strip()]
            cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

            print(cleaned_raw_text)

            print("===============")
            break


@app.route("/api/python")
def hello_world():
    def generate():
        client = OpenAI()
        target_language = '中文'
        print(cleaned_raw_text)
        prompt = f"翻译为{target_language}：{cleaned_raw_text}"
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


def generate():
    tokens = cleaned_raw_text.split(" ")
    for token in tokens:
        time.sleep(0.2)
        yield f"data: {token}\n\n"
    yield "data: [DONE]\n\n"


@app.route('/api/stream')
def stream():
    response = Response(generate(), mimetype='text/event-stream')
    return response


if __name__ == "__main__":
    app.run(debug=True)
