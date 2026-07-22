# [daad](): [D]()iscord [A]()NSI [ad]()apter

Converts ANSI color escape sequences from stdin into the limited 4-bit sequences supported by discord.
Selects the Discord color with the lowest Euclidian distance to the target color.

## Demo

```sh
git diff --color=always
```

![image](https://github.com/user-attachments/assets/6be07cee-fc2a-4437-a623-23adc6dc2f01)

```sh
git diff --color=always | discord-ansi-adapter | discord-message
```

![image](https://github.com/user-attachments/assets/941d3594-b8a0-4f0f-9944-02e70b4b209c)

## Usage

```sh
some command here | discord-ansi-adapter
```

<details><summary>To use the primitive message sending helper script:</summary>

```sh
# setup a discord bot
export DISCORD_BOT_TOKEN='...'
export DISCORD_CHANNEL_ID='...'
some command here | discord-message
```

</details>

## Installation

using [uv](https://github.com/astral-sh/uv):

```shell
uv tool install git+https://github.com/simonLeary42/daad
```

using `pip`:

```shell
pip install git+https://github.com/simonLeary42/daad
```
