#!/bin/env python3
import os
import sys
import time
import textwrap
import traceback
import discord
import json

DISCORD_MESSAGE_CHAR_LIMIT = 2000
AFTER_MESSAGE_SLEEP_SECONDS = 0.2

if os.path.exists(".env.json"):
    with open(".env.json", "r", encoding="utf8") as f:
        os.environ.update(json.load(f))

TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
intents = discord.Intents.default()
client = discord.Client(intents=intents)

text_wrapper = textwrap.TextWrapper(
    break_long_words=False,
    break_on_hyphens=False,
    replace_whitespace=False,
    width=DISCORD_MESSAGE_CHAR_LIMIT,
)
_input = sys.stdin.read()

# make sure that any one line will fit in one message
_input_lines = []
for line in _input.splitlines():
    # +1 for trailing newline
    if len(line) + 1 > DISCORD_MESSAGE_CHAR_LIMIT:
        _input_lines.extend(text_wrapper.wrap(line))
    else:
        _input_lines.append(line)


messages = []
current_message = "```ansi\n"
for i, line in enumerate(_input_lines):
    if len(current_message) + len(f"{line}\n```") > DISCORD_MESSAGE_CHAR_LIMIT:
        messages.append(current_message + "```")
        current_message = "```ansi\n"
    current_message += line + "\n"
messages.append(current_message + "```")


@client.event
async def on_ready():
    print(f"Logged in as {client.user}", file=sys.stderr)
    if not (channel := client.get_channel(CHANNEL_ID)):
        raise RuntimeError("Channel not found. Check the ID.")
    try:
        for message in messages:
            # print(f"message:\n{message}\nend of message")
            await channel.send(message)
            time.sleep(AFTER_MESSAGE_SLEEP_SECONDS)
    except discord.errors.HTTPException:
        traceback.print_exc()
        sys.exit(1)
    await client.close()


client.run(TOKEN)
