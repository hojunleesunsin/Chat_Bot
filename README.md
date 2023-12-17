![Chat Bot을 이용한 작업일지 APP](https://capsule-render.vercel.app/api?type=waving&color=auto&height=300&section=header&text=Chat%20Bot을%20이용한%20작업일지%20APP&fontSize=40)

## 목차
- [목차](#목차)
- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [프로젝트 목표](#프로젝트-목표)
- [기술 스택](#기술-스택)
  - [Flask](#flask)
  - [MongoDB](#mongodb)
- [프로젝트 결론](#프로젝트-결론)
- [프로젝트 문제점](#프로젝트-문제점)

<br>
<br>

## 프로젝트 개요
사용자가 작업일지를 작성하고 작업일지에 대한 내용을 수정, 조회, 삭제하는 기능을 제공합니다.

## 주요 기능
- 사용자가 앱에서 작업일지를 작성하고 mongoDB에 저장해주는 기능
- 저장된 데이터를 기준으로 조회, 수정, 삭제해주는 기능
- ChatBot을 활용해 앱에서 작성한 내용을 서버에서 mongoDB에 저장해주는 기능

## 프로젝트 목표
팀 프로젝트로 Flask 서버 숙련도 향상 및 CRUD 구현을 위해 진행하였고 사용자가 편리하게 자신의 작업에 대한 일지를 작성하고 확인, 수정, 삭제할 수 있도록 기능을 제공하는 것이 목표입니다.

## 기술 스택
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" width="50%" height="150"><img src="https://img.shields.io/badge/mongoDB-47A248?style=for-the-badge&logo=MongoDB&logoColor=white" width="50%" height="150">

<br>
<br>
<br>

***
### Flask
Flask 서버를 이용하여 앱으로부터 들어온 요청에 맞게 CRUD 기능을 수행한다.  
앱으로부터 classify_text 요청을 받아 전달 받은 텍스트를 학습된 ChatBot 모델에 적용 시킨후 나온 결과 값을 mongoDB에 저장하고 결과 값을 mongoDB에 저장한다.

- 정보를 저장 해주는 기능
  - 앱으로 부터 전달 받은 데이터를 기반으로 저장한다.
  
```python
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
```
- 정보를 조회 해주는 기능
  - 앱으로부터 전달 받은 데이터를 기반으로 데이터를 조회하여 앱에 전송한다.
```python
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
```

- 정보를 삭제 해주는 기능
  - 앱으로부터 전달받은 ObjectId를 기반으로 mongoDB에서 데이터를 삭제한다.
 
```python
@socketio.on('delete_info')
def delete_Info(data):
    try:
        if "id" in data:
            document_id = ObjectId(data["id"])
            existing_data = 
            collection.count_documents({"_id": document_id})

            if existing_data > 0:
                collection.delete_one({"_id": document_id})
                socketio.emit('delete_result',
                 {"message": "성공적으로 삭제되었습니다."})
            else:
                socketio.emit('delete_error', 
                {"message": "존재하지 않는 데이터 입니다."})
    except Exception as e:
        socketio.emit('delete_error',
         {"message": f"데이터를 삭제하던 중 오류 발생: {e}"})
```

- 정보를 수정 해주는 기능
  - 앱으로부터 전달받은 ObjectId를 기반으로 mongoDB에서 데이터를 수정한다. 
```python
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
```


<br>

### MongoDB
flask와 mongoDB를 연동하여 앱으로 부터 들어온 값들을 저장, 검색, 수정, 삭제 기능을 수행한다.

## 프로젝트 결론

## 프로젝트 문제점