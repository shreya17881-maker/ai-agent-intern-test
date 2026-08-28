from app.agent import AsterRowAgent


agent = AsterRowAgent()


print("\n==============================")
print("MULTI-TURN TEST")
print("==============================")


questions = [
    "Where is ORD-1007?",
    "When will it arrive?",
    "What is its current status?",
]


for question in questions:

    print("\nUSER:")
    print(question)

    answer = agent.ask(question)

    print("\nAGENT:")
    print(answer)
