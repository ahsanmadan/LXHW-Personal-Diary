from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime


client = MongoClient("mongodb+srv://test:asan@cluster0.hmhssac.mongodb.net/?retryWrites=true&w=majority")

db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")
    
    today = datetime.now()
    timenow = today.strftime(f"%d%m%Y%H%M%S")
    file = request.files["file_give"]
    extension = file.filename.split(".")[-1]
    filename = f'static/post-{timenow}.{extension}'
    file.save(filename)

    pp = request.files["pp_give"]
    extension = pp.filename.split(".")[-1]
    ppname = f'static/pp-{timenow}.{extension}'
    pp.save(ppname)

    time = today.strftime("%d-%m-%Y")

   

    doc = {
        "file": filename,
        "pp" : ppname,
        "title": title_receive,
        "content": content_receive,
        "time": time,
        
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'Berhasil Di Post!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
