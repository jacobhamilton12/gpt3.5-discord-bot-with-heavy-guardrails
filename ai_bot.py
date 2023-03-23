import openai
import os
import sys
import tiktoken
from misc import retry, timeout
from logger import logger
sys.path.append('/home/jake/')


openai.api_key = os.environ.get('OPENAI_KEY')

MAX_TOKENS = 4000
MIN_TOKENS = 500
MAX_MESSAGE = 3000

class Bot:

    def __init__(self, init_prompt="You are a helpful assistant"):
        self.message_log = []
        self.send_to_openai(init_prompt, role='system', output_token_length=10)

    def token_count(self, model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
            num_tokens = 0
            for message in self.message_log:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
    See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


    @retry(num_retries=3, wait_seconds=5)
    @timeout(seconds=30)
    def send_to_openai(self, content, role='user', save_mem=True, output_token_length=4000):
        if len(content) > MAX_MESSAGE:
            return "Message too long, ignoring it"
        self.message_log.append({"role": role, "content": content})
        leftover_tokens = MAX_TOKENS - self.token_count()

        while leftover_tokens < MIN_TOKENS:
            # don't pop the first item, which is the system prompt
            self.message_log.pop(1)
            leftover_tokens = MAX_TOKENS - self.token_count()

        # Use OpenAI's ChatCompletion API to get the chatbot's response
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.message_log,
                max_tokens=min(leftover_tokens, output_token_length),
                stop=None,
                temperature=0.7,
            )
        except Exception as e:
            logger.exception(f"error sending to openai {repr(e)} {str(e)}")
            raise
        resp_msg = response.choices[0].message.content
        if save_mem:
            self.message_log.append({"role": "assistant", "content": resp_msg})
        else:
            self.message_log = self.message_log[:1]
        return resp_msg
