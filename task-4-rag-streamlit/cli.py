if __name__ == "__main__":
    from chat_bot import ChatBot
    from constants import details

    bot = ChatBot(context_details=details)

    while True:
        question = input("User : ")
        if question == "quit":
            break
        answer = bot.get_answer(question)

        print(f"Bot: {answer}")

    print("program ended successfully.")