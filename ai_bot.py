import openai
import os
import sys
sys.path.append('/home/jake/antitheist_bot')

from misc import retry

openai.api_key = os.environ.get('OPENAI_KEY')

MAX_TOKENS = 4000
MIN_TOKENS = 500

class Bot:
    
    def __init__(self, init_prompt="You are a helpful assistant"):
    # key words to block to keep ai on task / sound more natural
        self.message_log = []
        self.send_to_openai(init_prompt, role='system', output_token_length = 10)

    def token_count(self):
        count = 0
        for entry in self.message_log:
            count += len(entry["content"]) // 4 # 1 token is roughly 4 characters in english
        return count

    # Function to send a message to the OpenAI chatbot model and return its response
    @retry(num_retries=3, wait_seconds=5)
    def send_to_openai(self, content, role='user', save_mem=True, output_token_length = 4000):
        self.message_log.append({"role": role, "content": content})
        leftover_tokens =  MAX_TOKENS - self.token_count()
        while leftover_tokens < MIN_TOKENS:
            # don't pop first which is the system prompt
            self.message_log.pop(1)
            leftover_tokens =  MAX_TOKENS - self.token_count()
        # Use OpenAI's ChatCompletion API to get the chatbot's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
            messages=self.message_log,   # The conversation history up to this point, as a list of dictionaries
            max_tokens= min(MAX_TOKENS-leftover_tokens, output_token_length),        # The maximum number of tokens (words or subwords) in the generated response
            stop=None,              # The stopping sequence for the generated response, if any (not used here)
            temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
        )
        resp_msg = response.choices[0].message.content
        if save_mem:
            self.message_log.append({"role": "assistant", "content": resp_msg})
        return resp_msg

