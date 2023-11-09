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

# Corpus_File = "chat.txt"

# text = "6월 34일, 서울시 강남구 서초동 30-5, 금영 주식회사, 36,000원."
# sub = "기타 내용."

# chatbot = ChatBot("chatpot")

# trainer = ListTrainer(chatbot)
# # trainer = ([
# #     "Hi",
# #     "Welcome, My friend",
# # ])
# # trainer.train([
# #     "Are you Plant?",
# #     "No, I'm the pot below the plant",
# # ])

# clean_corpus = clean_corpus(Corpus_File)
# trainer.train(clean_corpus)
# # 프로젝트 주요 텍스트 분류 코드
# @app.route('/classify_text', methods=['POST'])
# def classify_text():
#     data = request.get_json()
#     text = data.get('text')
#     sub = data.get('sub')

#     exit_conditions = ("q", "quit", "exit")
#     while True:
#         query = input("> ")
#         if query in exit_conditions:
#             break
#         if not text:
#             print("text is empty")
#         else :
#             response = trainer.train(tc(text, sub))
#             print(f"{chatbot.get_response(query)}")
#             return jsonify({'response': response})

        
@app.errorhandler(Exception)
def handle_error(error):
    # 오류 발생 시 서버가 종료되지 않도록 처리
    app.logger.error(f"An error occurred: {str(error)}")
    return jsonify({"message": "서버에서 오류가 발생했습니다."}), 500
        
@app.route('/insert', methods=['POST'])
def insert_Info():
    try:
        data = request.get_json()
        if data:
            year = data.pop("year", None)  # "year" 키를 삭제하고 해당 값을 변수에 저장
            month = data.pop("month", None)  # "month" 키를 삭제하고 해당 값을 변수에 저장
            day = data.pop("day", None)  # "day" 키를 삭제하고 해당 값을 변수에 저장
            hour = data.pop("hour", None)  # "hour" 키를 삭제하고 해당 값을 변수에 저장
            minute = data.pop("minute", None)  # "minute" 키를 삭제하고 해당 값을 변수에 저장
            date_time = datetime.datetime(year, month, day, hour, minute)
            data["date_time"] = date_time 
            # 중복 데이터 확인: name, age, address 모두 동일한 경우 중복으로 처리
            # existing_data = collection.find_one({"name": data["name"], "age": data["age"], "address": data["address"], "cost": data["cost"]})
            # if existing_data:
            #     print("중복 데이터를 입력하였습니다.")
            #     return jsonify({"message": "이미 저장된 데이터 입니다."}), 400
            # else:
            collection.insert_one(data)
            return jsonify({"message": "데이터가 성공적으로 MongoDB에 저장되었습니다."}), 201
        else:
            print("JSON 형식 데이터가 제공되지 않았습니다.")
            return jsonify({"message": "유효한 JSON 데이터가 제공되지 않았습니다."}), 400
    except Exception as e:
        return jsonify({"message": f"데이터를 MongoDB에 저장하는 중 오류 발생: {e}"}), 500
    

@app.route('/select', methods=['POST'])
def select_Info():
    try:
        data = request.get_json()
        #입력한 데이터 DB에 있는지 확인
        result = collection.find({"name": data["name"], "age": data["age"], "address": data["address"]})
        if result:
            result_list = list(result)
            for item in result_list:
            # ObjectId를 문자열로 변환
                item['_id'] = str(item['_id'])
                
                # date_time 필드를 원하는 형식으로 포맷
                item['date_time'] = item['date_time'].strftime("%a, %d %b %Y %H:%M")
                #보여주지 않아도 되는 데이터 제거
                # item.pop('_id', None)
                # item.pop('cost', None)
            print(result_list)
            print("데이터를 찾아서 전송했습니다.")
            return jsonify(result_list)
        else:
            return jsonify({"message": "해당 데이터가 존재하지 않습니다."}), 400
    except Exception as e:
        return jsonify({"message": f"데이터를 MongoDB에 읽어오던 중 오류 발생: {e}"}), 500

    
@app.route('/delete', methods=['POST'])
def delete_Info():
    try:
        data = request.get_json()
        if data:
            year = data.pop("year", None)  # "year" 키를 삭제하고 해당 값을 변수에 저장
            month = data.pop("month", None)  # "month" 키를 삭제하고 해당 값을 변수에 저장
            day = data.pop("day", None)  # "day" 키를 삭제하고 해당 값을 변수에 저장
            hour = data.pop("hour", None)  # "hour" 키를 삭제하고 해당 값을 변수에 저장
            minute = data.pop("minute", None)  # "minute" 키를 삭제하고 해당 값을 변수에 저장
            date_time = datetime.datetime(year, month, day, hour, minute)
            data["date_time"] = date_time
            existing_data = collection.count_documents({"date_time": data["date_time"], "name": data["name"], "age": data["age"], "cost": data["cost"]})
            if existing_data > 0:
                collection.delete_one({"date_time": data["date_time"], "name": data["name"], "age": data["age"], "cost": data["cost"]})
                print("DB에서 데이터를 삭제하였습니다.")
                return jsonify({"message": "성공적으로 삭제되었습니다."})
            else:
                print("존재하지 않는 데이터입니다.")
                return jsonify({"message": "존재하지 않는 데이터 입니다."}), 400
    except Exception as e:
        return jsonify({"message": f"데이터를 삭제하던 중 오류 발생: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)