import numpy as np
import random
from tensorflow import keras
import nltk
from nltk.stem.lancaster import LancasterStemmer
nltk.download('punkt')
stemmer = LancasterStemmer()
from Data_PreProcess import Data_PreProcess
from bag_of_words import bag_of_words
from Main_Text_Classification_Model import Text_Classification

# pip install git+https://github.com/ssut/pu-hanspell.git

from hanspell import spell_checker

sent = '맞춤법이 틀린 한국어 문장'
spelled_sent = spell_checker.check(sent)
hanspell_sent = spelled_sent.checked

print(hanspell_sent)

words, labels, data = Data_PreProcess()

model = keras.models.load_model("Chat_Bot.h5")

exit_conditions = ("q", "quit", "exit")

def chat():
    print("Start talking with your bot (type quit to stop)!")
    while True:
        input_data = input(">: ")
        q_check = sepll_ckecker.check(input_data)
        q = q_check.checked
        if q in exit_conditions:
            break

        ret = model.predict(np.array([bag_of_words(q, words)]))
        ret_index = np.argmax(ret)
        tag = labels[ret_index]

        responses = []
        for tg in data["intents"]:
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
    # 이거는 어디다 둬야할지 고민중임
    print("Your request Data is it?:", Update_Data)

chat()
