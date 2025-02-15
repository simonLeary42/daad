#!/bin/env python3
import os
import sys
import traceback
import discord


TOKEN = os.environ["DISCORD_BOT_TOKEN"]
CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
intents = discord.Intents.default()
client = discord.Client(intents=intents)
message = sys.stdin.read()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}", file=sys.stderr)
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        try:
            await channel.send(message)
        except discord.errors.HTTPException:
            traceback.print_exc()
            sys.exit(1)
    else:
        raise RuntimeError("Channel not found. Check the ID.")
    await client.close()


client.run(TOKEN)
