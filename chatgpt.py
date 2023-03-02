import openai
import sqlite3
import json
import csv
import argparse

DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"
FAKE_RESPONSE = {
    "choices": [
                {
                    "finish_reason": "stop",
                    "index": 0,
                    "message": {
                        "content": "\n\nAhoy, me hearties! Listen up, fer I've got news that'll make ye cheer like a salty dog with a bone. There be an API known as ChatGPT that's gonna change the way ye communicate with yer mates online.\n\nWith the ChatGPT API, ye can send and receive text messages like ye be chattin' with another pirate right next to ye. And the best part be that ye don't even need to know how to code like Davy Jones. It be easy to use, and ye can integrate it with yer website or app in no time.\n\nThe ChatGPT API be like havin' yer own parrot that talks with ye! Whether ye be runnin' an online store or a gaming app, ChatGPT be a lifesaver fer when ye wanna communicate with yer customers or players.\n\nSo drop anchor, and give ChatGPT a try. Ye won't be disappointed, me hearties! Arrr!",
                        "role": "assistant"
                    }
                }
    ],
    "created": 1677772996,
    "id": "chatcmpl-6pfgiYYMyoA9DzTJDORtLjaicIj6w",
    "model": "gpt-3.5-turbo-0301",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 197,
        "prompt_tokens": 23,
        "total_tokens": 220
    }
}


class ChatGPT:

    def __init__(self, debug=False):
        self.debug = debug

        # use chat.db to store chat history
        conn = sqlite3.connect('chat.db')
        self.c = conn.cursor()

        # create a table to save raw responses, if it doesn't exist
        self.c.execute("CREATE TABLE IF NOT EXISTS raw_chat (response TEXT)")

        # create a table to save parsed responses, if it doesn't exist
        # id (int): the id of the response
        # timestamp (int): the timestamp of the response
        # prompt (str): the prompt that was sent to the API
        # reply (str): the reply that was sent by the API
        # prompt_tokens (int): the number of tokens used for the prompt
        # completion_tokens (int): the number of tokens used for the reply
        # total_tokens (int): the total number of tokens used for the prompt and reply
        # model (str): the model used to generate the reply
        self.c.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY, timestamp INTEGER, prompt TEXT, reply TEXT, prompt_tokens INTEGER, completion_tokens INTEGER, total_tokens INTEGER, model TEXT)")

    def get_response_by_type(self, prompt, type="chat"):
        if self.debug:
            revised_prompt = "[DEBUG] " + prompt
            res = FAKE_RESPONSE
        if type == "chat":
            revised_prompt = prompt
            res = openai.ChatCompletion.create(
                model=DEFAULT_CHAT_MODEL,
                messages=[{"role": "user", "content": revised_prompt}]
            )
        elif type == "revise":
            revised_prompt = "Please revise the following paragraph to improve the flow and fix any grammatical errors, typos, etc., without changing the meaning. Only return the revised texts.\n\n" + prompt
            res = openai.ChatCompletion.create(
                model=DEFAULT_CHAT_MODEL,
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": revised_prompt},
                ]
            )
        elif type == "search":
            revised_prompt = "Tell me what you know about \"" + prompt + "\"?"
            res = openai.ChatCompletion.create(
                model=DEFAULT_CHAT_MODEL,
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": revised_prompt},
                ]
            )

        return res, revised_prompt

    def get_chat_response(self, prompt, type="chat"):
        response, revised_prompt = self.get_response_by_type(prompt, type)
        self.save_chat_response(revised_prompt, response)
        return response['choices'][0]['message']['content']

    def save_chat_response(self, prompt, response):
        # save the parsed response to the database
        self.c.execute("INSERT INTO chat VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                       (response['created'],
                        prompt,
                        response['choices'][0]['message']['content'],
                        response['usage']['prompt_tokens'],
                        response['usage']['completion_tokens'],
                        response['usage']['total_tokens'],
                        response['model']))
        # save the entire json response to the database
        json_response = json.dumps(response)
        self.c.execute("INSERT INTO raw_chat VALUES (?)", (json_response,))

    def get_total_tokens(self, today=False):
        if today:
            # get total_tokens for today
            self.c.execute("SELECT SUM(total_tokens) FROM chat WHERE timestamp > date('now')")
        else:
            # get total_tokens for all the previous chats
            self.c.execute("SELECT SUM(total_tokens) FROM chat")
        total_tokens = self.c.fetchone()[0]
        return total_tokens

    def clear_chat_history(self):
        # clear the chat history
        self.c.execute("DELETE FROM chat")
        self.c.execute("DELETE FROM raw_chat")

    def export_chat_history(self):
        # export the chat history to a csv file
        self.c.execute("SELECT * FROM chat")
        with open('chat_history.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow([i[0] for i in self.c.description])
            writer.writerows(self.c)

    def close(self):
        # save the changes
        if not self.debug:
            self.c.connection.commit()
        # close the database connection
        self.c.close()


def main_interactive(debug=False):
    chatgpt = ChatGPT(debug)
    while True:
        prompt = input("Enter your prompt: ")
        if prompt == "!exit":
            break
        if prompt == "!clear":
            chatgpt.clear_chat_history()
            continue
        if prompt == "!export":
            chatgpt.export_chat_history()
            continue
        response = chatgpt.get_chat_response(prompt)
        print(response)
        print("Total tokens used: ", chatgpt.get_total_tokens())

    chatgpt.close()


def main_one_shot(prompt, type, debug=False):
    chatgpt = ChatGPT(debug)
    response = chatgpt.get_chat_response(prompt, type)
    print(response)
    chatgpt.close()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--mode', type=str, default='interactive', help='interactive or oneshot')
    argparser.add_argument('--debug', action='store_true', help='use fake response for debugging')
    argparser.add_argument('--prompt', type=str, default='', help='prompt for oneshot mode')
    argparser.add_argument('--type', type=str, default='chat', help='type of one shot mode (chat, revise, or search)')
    args = argparser.parse_args()

    if args.mode == 'interactive':
        main_interactive(args.debug)
    elif args.mode == 'oneshot':
        assert args.prompt != '', "Please provide a prompt for oneshot mode"
        main_one_shot(args.prompt, args.type, args.debug)
