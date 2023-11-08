from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from cleaner import clean_corpus
from Main_Text_Classification_Model import text_classifier as tc

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
trainer.train(tc(text, sub))

exit_conditions = ("q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"{chatbot.get_response(query)}")