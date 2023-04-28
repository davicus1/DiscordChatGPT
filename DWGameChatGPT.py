###################################
# Author David Wyman
# 2023
# License: MIT-0
###################################
import os
import discord
import openai
from discord.ext import (commands)
from dotenv import load_dotenv
###
# Suggestion to ChatGPT to limit the scope of responses. This would be a good thing to pass as a separate API parameter
###
suggested_limit = "Limited to PC Games and 1000 characters,"

# dotenv to expand POSIX OS parameters
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv('OPENAPI_KEY')

# Discord Intents manage access to features. Without this, the Bot can't read the messages
intents = discord.Intents.default()
intents.message_content = True

# Initialize the Bot
bot = commands.Bot(command_prefix="!", intents=intents)


def application(start_response):
    status = '200 OK'
    output = b'TEST!\n'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


@bot.event
async def on_ready():
    print(f'We have logged to discord in as {bot.user}')


def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=suggested_limit + " " + prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


@bot.command()
async def test(ctx):
    print('test command received')
    await ctx.send('TEST!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f'Message Received Sir!: {message.author}::{message.content}')
    #TODO A command seems to only pass the first word, unless you quote it. This !chat in on_message is a workaround but causes an error in the log. Need to improve this
    if message.content.startswith('!chat'):
        chat_message = message.content[5:].strip()
        response = generate_response(chat_message)
        await message.channel.send(response)
    elif message.content.startswith("Hello"):
        await message.channel.send('Hello!')
    await bot.process_commands(message)


bot.run(TOKEN)
