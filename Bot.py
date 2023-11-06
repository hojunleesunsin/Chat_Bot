from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("chatpot")

trainer = ListTrainer(chatbot)
trainer = ([
    "Hi",
    "Welcome, My friend",
])
trainer.train([
    "Are you Plant?",
    "No, I'm the pot below the plant",
])

exit_conditions = ("q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"{chatbot.get_response(query)}")