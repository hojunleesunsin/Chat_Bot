from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pymongo import MongoClient
import datetime
from Main_Text_Classification_Model import text_classifier as tc
from Bot import chat

mongo_connect = "mongodb+srv://hongpc0099:hoz26064247@worklog.dxlbirn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_connect)
db = mongo_connect["WorkLog"]
collection = db["Info"]


app = Flask(__name)

Corpus_File = "chat.txt"

text = "6월 34일, 서울시 강남구 서초동 30-5, 금영 주식회사, 36,000원."
sub = "기타 내용."

chatbot = ChatBot("chatpot")

trainer = ListTrainer(chatbot)
# trainer = ([
#     "Hi",
#     "Welcome, My friend",
# ])
# trainer.train([
#     "Are you Plant?",
#     "No, I'm the pot below the plant",
# ])

clean_corpus = clean_corpus(Corpus_File)
trainer.train(clean_corpus)
# 프로젝트 주요 텍스트 분류 코드
@app.route('/classify_text', methods=['POST'])
def classify_text():
    data = request.get_json()
    text = data.get('text')
    sub = data.get('sub')

    exit_conditions = ("q", "quit", "exit")
    while True:
        query = input("> ")
        if query in exit_conditions:
            break
        if not text:
            print("text is empty")
        else :
            response = trainer.train(tc(text, sub))
            print(f"{chatbot.get_response(query)}")
            return jsonify({'response': response})
        
@app.route('/insert', methods=['POST'])
def insert_Info():
    try:
        data = request.get_json()
        if data:
            collection.insert_one(data)
        else:
            return jsonify({"message": "유효한 JSON 데이터가 제공되지 않았습니다."}), 400
    except Exception as e:
        return jsonify({"message": f"데이터를 MongoDB에 저장하는 중 오류 발생: {e}"}), 500
    




if __name__ == '__main__':
    app.run(debug=True)