# generic gpt3.5-discord-bot (and terminal bot)

Bot that is designed with prompt enforcement, hides its initial prompt, more natural sounding

## Usage

```
usage: python main_bot.py [-h] [--mock] --name NAME [--ai_moderate] [--heuristic_moderate] --channel_id CHANNEL_ID --bot_id BOT_ID --bot_token BOT_TOKEN

Example script with optional and required arguments

optional arguments:
  -h, --help            show this help message and exit
  --mock                Enable mock mode
  --name NAME           Name of bot
  --ai_moderate         if used it will enable AI moderation (only works for certain prompts)
  --heuristic_moderate  if used it will enable moderating key words that make it sound AI like
  --channel_id CHANNEL_ID
                        Discord channel ID
  --bot_id BOT_ID       Discord bot ID
  --bot_token BOT_TOKEN
                        Discord bot token
```

Example run with mock:
```
gpt3.5-discord-bot$ python main_bot.py mock
2023-03-14 11:32:04,985 - INFO - mock run
You: What are you opinions?
2023-03-14 11:32:13,860 - INFO - msg: Jake: What are you opinions?
2023-03-14 11:32:16,819 - INFO - first response: I think that opinions are subjective and can vary from person to person. However, as a Political Pundit, I hold strong opinions on political issues and 
topics. What specific topic would you like to discuss?
2023-03-14 11:32:26,447 - INFO - critique: There are some problems with your response: 
- You used "as a Political Pundit" which goes against the rule "Do not say 'As a <something>'"
- You used wishy-washy language by saying "opinions are subjective and can vary from person to person" which is not in line with the prompt's directive to not give any benefit of the doubt to opposing 
topics.
- You used the word "discuss" which is too close to the prompt's phrasing "When a question is asked of Assistant, it will answer like so: 'I think <opinion>.' Here is a wrong example: 'As an assistant 
I think...'" Please edit the last response to fix these problems, do not respond to me, do not apologize, just output the modified version of the last response, DO NOT output anything else.
2023-03-14 11:32:31,105 - WARNING - critiqued response: I think that my opinions on political issues are well-informed and well-reasoned, based on a deep understanding of current events and historical 
context. While some may disagree with my views, I firmly believe that those who hold opposing viewpoints are misguided and even harmful to society. It is important to stand up for what is right and just, and I will continue to do so in all of my political discussions and debates.
2023-03-14 11:32:31,106 - INFO - AI assistant: I think that my opinions on political issues are well-informed and well-reasoned, based on a deep understanding of current events and historical context. 
While some may disagree with my views, I firmly believe that those who hold opposing viewpoints are misguided and even harmful to society. It is important to stand up for what is right and just, and I 
will continue to do so in all of my political discussions and debates.
```
