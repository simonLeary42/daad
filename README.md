# [daad](): [D]()iscord [A]()NSI [ad]()apter

converts ANSI color escape sequences from stdin into the limited 4-bit sequences supported by discord.

selects the Discord color with the lowest Euclidian distance to the target color.

## example:

```sh
git diff --color=always | discord-ansi-adapter.py | discord-message.py
```

![image](https://github.com/user-attachments/assets/6be07cee-fc2a-4437-a623-23adc6dc2f01)

![image](https://github.com/user-attachments/assets/941d3594-b8a0-4f0f-9944-02e70b4b209c)
