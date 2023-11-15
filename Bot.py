import random
from BotLib_fc.Main_Text_Classification_Model import Text_Classification
import json
# pip install git+https://github.com/ssut/pu-hanspell.git
# from hanspell.hanspell import spell_checker
# 한국어 품사 태깅
# pip install kss
# import kss
# kss.split_sentences(text)

exit_conditions = ("q", "그만", "종료")
with open('intents.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def help():
    responses = []

    for tg in data["intents"]:
        if tg['tag'] == 'Help':
            responses = tg.get('responses', [])
    if not responses:
        print("이해할 수 없습니다.")
    else:
        print(random.choice(responses))

def Main_text_Classificaion(input_data):
    Update_Data = {
        "time": None,
        "date": None,
        "address": None,
        "pay": None
    }
    classifier = Text_Classification(input_data, None)
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

def chat():
    print("챗봇을 실행합니다! (q, 그만, 종료와 같은 입력을 하면 종료합니다.)")
    while True:
        q = input(">: ")
        # q_check = spell_checker.check(input_data)
        # q = q_check.checked
        if q in exit_conditions:
            if q == "q":
                print(f"{q}? Ok, I understand. Program exit")
            else:
                print(f"{q}합니다.")
            break
        elif q.lower() == 'help':
            help()
        else:
            Main_text_Classificaion(q)

chat()
