import requests
import json

# insert test
# Flask 앱의 URL (로컬 또는 원격 서버 URL로 변경)
url = 'http://localhost:5000/insert'  # Flask 앱의 URL로 변경

# 보낼 JSON 데이터
data = {
    "year": 2022,
    "month": 11,
    "day": 9,
    "hour": 14,
    "minute": 55,
    "name": "이호준",
    "age": 24,
    "address": "불당 24로 38",
    "cost": 60000
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


#select test
# 서버 URL
server_url = "http://localhost:5000/select"  # 서버 주소와 포트를 실제 서버에 맞게 수정해야 합니다

# 클라이언트에서 검색할 데이터
search_data = {
    "name": "이호준",
    "age": 24,
    "address": "불당 24로 38",
    "cost": 50000
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


#delete test
# 클라이언트에서 삭제할 데이터 정보
data_to_delete = {
    "year": 2023,
    "month": 11,
    "day": 9,
    "hour": 14,
    "minute": 55,
    "name": "이호준",
    "age": 24,
    "address": "불당 24로 38",
    "cost": 60000
}

# 서버의 URL 설정
server_url = "http://localhost:5000/delete"  # 서버 주소와 엔드포인트에 맞게 수정

# POST 요청 보내기
response = requests.post(server_url, json=data_to_delete)

# 서버 응답 확인
if response.status_code == 200:
    print("서버로부터 성공적인 응답을 받았습니다.")
    print("응답 내용:", response.json())
elif response.status_code == 404:
    print("서버로부터 데이터가 존재하지 않는 응답을 받았습니다.")
    print("응답 내용:", response.json())
else:
    print("서버로부터 오류 응답을 받았습니다.")
    print("응답 내용:", response.json())
