# Discord ANSI Adapter

converts ANSI color escape sequences from stdin into the limited 4-bit sequences supported by discord.
rounds 256color and true color escape sequences to the colors displayed in the discord client using Euclidian distance.

## example:

```sh
git diff --color=always | discord-ansi-adapter.py | discord-message.py
```
