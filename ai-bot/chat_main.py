from chat_api import chat_def
from speech_to_text import take_command

if __name__ == '__main__':
    # Input from user
    # Make input to lowercase
    query = take_command()
    while query == "None":
        query = take_command()
    chat_def(query)
