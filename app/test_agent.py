from app.agent import AsterRowAgent


agent = AsterRowAgent()


questions = [
    "How many days do I have to return an item?",
    "Do you ship to Canada?",
    "Can I cancel my order?",
    "Where is ORD-1007?",
    "When will ORD-1007 arrive?",
    "Where is ORD-9999?",
    "Where is my order?",
]


for question in questions:

    print("\n================================")
    print("QUESTION:", question)
    print("================================")

    answer = agent.ask(question)

    print("\nANSWER:")
    print(answer)
