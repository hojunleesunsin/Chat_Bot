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


app = Flask(__name__)

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
            # 중복 데이터 확인: name, age, address 모두 동일한 경우 중복으로 처리
            existing_data = collection.find_one({"name": data["name"], "age": data["age"], "address": data["address"]})
            if existing_data:
                print("중복 데이터를 입력하였습니다.")
                return jsonify({"message": "이미 저장된 데이터 입니다."}), 400
            else:
                collection.insert_one(data)
                return jsonify({"message": "데이터가 성공적으로 MongoDB에 저장되었습니다."}), 201
        else:
            print("JSON 형식 데이터가 제공되지 않았습니다.")
            return jsonify({"message": "유효한 JSON 데이터가 제공되지 않았습니다."}), 400
    except Exception as e:
        return jsonify({"message": f"데이터를 MongoDB에 저장하는 중 오류 발생: {e}"}), 500
    

@app.route('/search', methods=['POST'])
def search_Info():
    try:
        data = request.get_json()
        result = collection.find_one({"name": data["name"], "age": data["age"], "address": data["address"]})
        
        if result:
            # ObjectId를 문자열로 변환
            result['_id'] = str(result['_id'])
            # result.pop('_id', None)
            return jsonify(result)
        else:
            return jsonify({"message": "해당 데이터가 존재하지 않습니다."}), 400
            
            
    except Exception as e:
        return jsonify({"message": f"데이터를 MongoDB에 읽어오던 중 오류 발생: {e}"}), 500
if __name__ == '__main__':
    app.run(debug=True)