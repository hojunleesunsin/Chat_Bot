import numpy as np
import random
from tensorflow import keras
import nltk
from nltk.stem.lancaster import LancasterStemmer
nltk.download('punkt')
stemmer = LancasterStemmer()
from BotLib_fc.Data_PreProcess import Data_PreProcess
from BotLib_fc.bag_of_words import bag_of_words
from BotLib_fc.Main_Text_Classification_Model import Text_Classification
# pip install git+https://github.com/ssut/pu-hanspell.git
# from hanspell import spell_checker
# 한국어 품사 태깅
# pip install kss
# import kss
# kss.split_sentences(text)

words, labels, data,_ ,_ = Data_PreProcess()
# 모델 학습 다시 시켜야함
# intents.json 파일 변경, 현재 모델 학습에 문제가 있음 or tensorflow 문제있음
model = keras.models.load_model("Chat_Bot.h5")

exit_conditions = ("q", "quit", "exit", "그만", "종료")

def chat():
    print("입력을 시작하세요(q, quit, exit, 그만, 종료를 입력하면 종료됩니다.)!")
    while True:
        q = input(">: ")
        # q_check = spell_checker.check(input_data)
        # q = q_check.checked
        if q in exit_conditions:
            if q == "q" or q == "quit" or q == "exit":
                print(f"{q}? Ok I'm understand program exit")
            else:
                print(f"{q}합니다.")
            break

        ret = model.predict(np.array([bag_of_words(q, words)]))
        ret_index = np.argmax(ret)
        tag = labels[ret_index]

        responses = []

        for tg in data["intents.json"]:
            if tg['tag'] == tag:
                responses = tg.get('responses', [])
        if not responses:
            print("I'm Sorry, I dont understand")
        else:
            print(random.choice(responses))
    # 이거 DB에 저장하면 초기화 시켜줘야함
    Update_Data = {
        "time": None,
        "date": None,
        "address": None,
        "pay": None
    }
    classifier = Text_Classification(q, None)
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
        # 이거는 어디다 둬야할지 고민중임
        print("Your request Data is it?:", Update_Data)

chat()
