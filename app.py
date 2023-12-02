from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
from Bot import exit_conditions, help
from BotLib_fc.Main_Text_Classification_Model import Text_Classification as tc

mongo_connect = "mongodb+srv://hongpc0099:hoz26064247@worklog.dxlbirn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_connect)
db = client["WorkLog"]
collection = db["Info"]


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

Corpus_File = "chat.txt"

text = "6월 34일, 서울시 강남구 서초동 30-5, 36,000원."
sub = "기타 내용."

Update_Data = {
            "time": None,
            "date": None,
            "address": None,
            "pay": None
            }    

# 프로젝트 주요 텍스트 분류 코드
@socketio.on('classify_text')
def classify_text(data):
    try:
        text = data.get('text')

        if not text:
            socketio.emit('classification_error', {"message": "Text is empty"})
        elif text in exit_conditions:
            if text == "q":
                print(f"{text}? Ok, I understand. Program exit")
            else:
                print(f"{text}합니다.")
        elif text.lower() == 'help':
            help()
        else:
            classifier = tc(text, None)
            time = classifier.Time_Pattern()
            date = classifier.Date_Pattern()
            address = classifier.Address_Pattern()
            pay = classifier.Pay_Pattern()

            if time is not None:
                Update_Data["time"] = time
            if date is not None:
                Update_Data["date"] = date
            if address is not None:
                Update_Data["address"] = address
            if pay is not None:
                Update_Data["pay"] = pay

            if time is not None or date is not None or address is not None or pay is not None:
                print("당신이 작성한 내용이 이것이 맞습니까?:", Update_Data)

                collection.insert_one(Update_Data)

                # Update_Data를 초기화
                Update_Data = {
                    "time": None,
                    "date": None,
                    "address": None,
                    "pay": None
                }

                socketio.emit('classification_result', {"message": "데이터가 성공적으로 MongoDB에 저장되었습니다."})

    except Exception as e:
        socketio.emit('classification_error', {"message": f"데이터를 MongoDB에 저장하는 중 오류 발생: {e}"})

        
@app.errorhandler(Exception)
def handle_error(error):
    # 오류 발생 시 서버가 종료되지 않도록 처리
    app.logger.error(f"An error occurred: {str(error)}")
    return jsonify({"message": "서버에서 오류가 발생했습니다."}), 500
        
@socketio.on('insert_info')
def insert_Info(data):
    try:
        if data:
            year = data.pop("year", None)
            month = data.pop("month", None)
            day = data.pop("day", None)
            hour = data.pop("hour", None)
            minute = data.pop("minute", None)
            date_time = datetime(year, month, day, hour, minute)
            data["date_time"] = date_time

            collection.insert_one(data)
            socketio.emit('insert_result', {"message": "데이터가 성공적으로 MongoDB에 저장되었습니다."})
        else:
            socketio.emit('insert_error', {"message": "유효한 JSON 데이터가 제공되지 않았습니다."})

    except Exception as e:
        socketio.emit('insert_error', {"message": f"데이터를 MongoDB에 저장하는 중 오류 발생: {e}"})
    

@socketio.on('select_info')
def select_Info(data):
    try:
        query = {"$and": []}

        if data.get("name"):
            query["$and"].append({"name": data["name"]})
        if data.get("age"):
            query["$and"].append({"age": data["age"]})
        if data.get("address"):
            query["$and"].append({"address": data["address"]})
        if data.get("start_date") and data.get("end_date"):
            start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(data["end_date"], "%Y-%m-%d") + timedelta(days=1)
            query["$and"].append({"date_time": {"$gte": start_date, "$lte": end_date}})

        if not query["$and"]:
            socketio.emit('select_error', {"message": "적어도 하나의 검색 조건을 제공해야 합니다."})
        else:
            result = collection.find(query)
            count = collection.count_documents(query)

            if count > 0:
                result_list = list(result)
                for item in result_list:
                    item['_id'] = str(item['_id'])
                    item['date_time'] = item['date_time'].strftime("%a, %d %b %Y %H:%M")

                socketio.emit('select_result', result_list)
            else:
                socketio.emit('select_error', {"message": "해당 데이터가 존재하지 않습니다."})

    except Exception as e:
        socketio.emit('select_error', {"message": f"데이터를 MongoDB에 읽어오던 중 오류 발생: {e}"})
    

@socketio.on('delete_info')
def delete_Info(data):
    try:
        if "id" in data:
            document_id = ObjectId(data["id"])
            existing_data = collection.count_documents({"_id": document_id})

            if existing_data > 0:
                collection.delete_one({"_id": document_id})
                socketio.emit('delete_result', {"message": "성공적으로 삭제되었습니다."})
            else:
                socketio.emit('delete_error', {"message": "존재하지 않는 데이터 입니다."})
    except Exception as e:
        socketio.emit('delete_error', {"message": f"데이터를 삭제하던 중 오류 발생: {e}"})
    

@socketio.on('update_info')
def update_Info(data):
    try:
        if "id" in data:
            document_id = ObjectId(data["id"])
            existing_data = collection.count_documents({"_id": document_id})

            if existing_data > 0:
                update_data = data.get("update_data", {})

                if update_data:
                    collection.update_one({"_id": document_id}, {"$set": update_data})
                    socketio.emit('update_result', {"message": "성공적으로 업데이트되었습니다."})
                else:
                    socketio.emit('update_error', {"message": "업데이트할 데이터가 제공되지 않았습니다."})
            else:
                socketio.emit('update_error', {"message": "존재하지 않는 데이터 입니다."})
    except Exception as e:
        socketio.emit('update_error', {"message": f"데이터를 수정하던 중 오류 발생: {e}"})
    
if __name__ == '__main__':
    socketio.run(app, debug=True)