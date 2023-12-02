import requests
import json
from datetime import datetime

# Flask 앱의 URL (로컬 또는 원격 서버 URL로 변경)
url = "http://localhost:5000/insert"  # Flask 앱의 URL로 변경

# 보낼 JSON 데이터
data = {
    "year": 2022,
    "month": 11,
    "day": 30,
    "hour": 22,
    "minute": 30,
    "name": "한석규",
    "age": 35,
    "address": "쌍용 38로 12",
    "cost": 70000
}

# JSON 데이터를 Flask 앱으로 POST 요청을 보냄
response = requests.post(url, json=data)

# insert 응답 확인
if response.status_code == 201:
    print("데이터가 성공적으로 Flask 앱에 저장되었습니다.")
elif response.status_code == 400:
    print("이미 저장된 데이터입니다.")
else:
    print("데이터를 Flask 앱에 저장하는 중 오류 발생:", response.status_code)


# 서버 URL
server_url = "http://localhost:5000/select"  # 서버 주소와 포트를 실제 서버에 맞게 수정해야 합니다

start_date = datetime.strptime("2022-11-01", "%Y-%m-%d")
end_date = datetime.strptime("2022-11-10", "%Y-%m-%d")
# 클라이언트에서 검색할 데이터
search_data = {
    "name": "한석규",
    "address": "쌍용 38로 12",
    "age": 35,
    "start_date": start_date.strftime("%Y-%m-%d"), 
    "end_date": end_date.strftime("%Y-%m-%d")
}

try:
    # 서버에 POST 요청을 보냅니다.
    response = requests.post(server_url, json=search_data)

    if response.status_code == 200:
        # 요청이 성공하면 서버에서 반환한 데이터를 JSON 형식으로 파싱합니다.
        result = response.json()
        print("검색 결과:")
        print(result)
    else:
        # 요청이 실패한 경우 에러 메시지를 출력합니다.
        print("서버 응답 오류:", response.status_code)
        error_message = response.json()
        print("에러 메시지:", error_message.get("message"))

except requests.exceptions.RequestException as e:
    print("서버와의 통신 중 오류 발생:", e)
    
    

# 클라이언트에서 삭제할 데이터 정보
Data_To_Delete = {"id": '655cc09a814402b38ad6cdd2'}

# 서버의 URL 설정
server_url = "http://localhost:5000/delete"  # 서버 주소와 엔드포인트에 맞게 수정

# POST 요청 보내기
response = requests.delete(server_url, json=Data_To_Delete)

if response.status_code == 200:
    print("삭제 성공: ", response.json())
elif response.status_code == 400:
    print("삭제 실패: ", response.json())
else:
    print("삭제 실패: ", response.json())


import requests
import json

# 서버의 주소와 엔드포인트 설정
server_url = "http://localhost:5000/update"

# 업데이트할 데이터 및 문서 ID 설정
update_data = {"name": "NewName", "age": 30}
document_id = "ObjectId"  # 서버에서 실제 데이터베이스에서 사용되는 문서의 ID로 교체

# 요청 데이터 설정
request_data = {"id": document_id, "update_data": update_data}

# 서버에 HTTP POST 요청 보내기
response = requests.post(server_url, json=request_data)

# 서버의 응답 확인
if response.status_code == 200:
    print("업데이트 성공:", response.json())
else:
    print("업데이트 실패:", response.status_code, response.json())
