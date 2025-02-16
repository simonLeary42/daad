#!/bin/env python3
import os
import re
import sys
from math import sqrt
import colorsys

#commit
DEBUG = True

# https://stackoverflow.com/a/14693789/18696276
ANSI_ESCAPE_8BIT = re.compile(
    r"((?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~]))"
)

DISCORD_FG_HEX_TO_4BIT_INDEX = {
    "35373D": 30,  # gray
    "D21C24": 31,  # red
    "738A05": 32,  # green
    "A57705": 33,  # yellow
    "2076C7": 34,  # blue
    "C61B6F": 35,  # pink
    "259286": 36,  # cyan
    # "FFFFFF": 37,  # white
}

DISCORD_BG_HEX_TO_4BIT_INDEX = {
    "022029": 40,  # firefly dark blue
    "BD3612": 41,  # orange
    "475B62": 42,  # marble blue
    "536870": 43,  # greyish turquoise
    "708285": 44,  # gray
    "595AB7": 45,  # indigo
    "819090": 46,  # light gray
    "FCF4DC": 47,  # white
}

# fmt: off
FAKE_8BIT_INDEX_TO_HEX = [
    "#000000", "#800000", "#008000", "#808000", "#000080", "#800080", "#008080", "#c0c0c0",
    "#808080", "#ff0000", "#00ff00", "#ffff00", "#0000ff", "#ff00ff", "#00ffff", "#ffffff",
    "#000000", "#00005f", "#000087", "#0000af", "#0000d7", "#0000ff", "#005f00", "#005f5f",
    "#005f87", "#005faf", "#005fd7", "#005fff", "#008700", "#00875f", "#008787", "#0087af",
    "#0087d7", "#0087ff", "#00af00", "#00af5f", "#00af87", "#00afaf", "#00afd7", "#00afff",
    "#00d700", "#00d75f", "#00d787", "#00d7af", "#00d7d7", "#00d7ff", "#00ff00", "#00ff5f",
    "#00ff87", "#00ffaf", "#00ffd7", "#00ffff", "#5f0000", "#5f005f", "#5f0087", "#5f00af",
    "#5f00d7", "#5f00ff", "#5f5f00", "#5f5f5f", "#5f5f87", "#5f5faf", "#5f5fd7", "#5f5fff",
    "#5f8700", "#5f875f", "#5f8787", "#5f87af", "#5f87d7", "#5f87ff", "#5faf00", "#5faf5f",
    "#5faf87", "#5fafaf", "#5fafd7", "#5fafff", "#5fd700", "#5fd75f", "#5fd787", "#5fd7af",
    "#5fd7d7", "#5fd7ff", "#5fff00", "#5fff5f", "#5fff87", "#5fffaf", "#5fffd7", "#5fffff",
    "#870000", "#87005f", "#870087", "#8700af", "#8700d7", "#8700ff", "#875f00", "#875f5f",
    "#875f87", "#875faf", "#875fd7", "#875fff", "#878700", "#87875f", "#878787", "#8787af",
    "#8787d7", "#8787ff", "#87af00", "#87af5f", "#87af87", "#87afaf", "#87afd7", "#87afff",
    "#87d700", "#87d75f", "#87d787", "#87d7af", "#87d7d7", "#87d7ff", "#87ff00", "#87ff5f",
    "#87ff87", "#87ffaf", "#87ffd7", "#87ffff", "#af0000", "#af005f", "#af0087", "#af00af",
    "#af00d7", "#af00ff", "#af5f00", "#af5f5f", "#af5f87", "#af5faf", "#af5fd7", "#af5fff",
    "#af8700", "#af875f", "#af8787", "#af87af", "#af87d7", "#af87ff", "#afaf00", "#afaf5f",
    "#afaf87", "#afafaf", "#afafd7", "#afafff", "#afd700", "#afd75f", "#afd787", "#afd7af",
    "#afd7d7", "#afd7ff", "#afff00", "#afff5f", "#afff87", "#afffaf", "#afffd7", "#afffff",
    "#d70000", "#d7005f", "#d70087", "#d700af", "#d700d7", "#d700ff", "#d75f00", "#d75f5f",
    "#d75f87", "#d75faf", "#d75fd7", "#d75fff", "#d78700", "#d7875f", "#d78787", "#d787af",
    "#d787d7", "#d787ff", "#d7af00", "#d7af5f", "#d7af87", "#d7afaf", "#d7afd7", "#d7afff",
    "#d7d700", "#d7d75f", "#d7d787", "#d7d7af", "#d7d7d7", "#d7d7ff", "#d7ff00", "#d7ff5f",
    "#d7ff87", "#d7ffaf", "#d7ffd7", "#d7ffff", "#ff0000", "#ff005f", "#ff0087", "#ff00af",
    "#ff00d7", "#ff00ff", "#ff5f00", "#ff5f5f", "#ff5f87", "#ff5faf", "#ff5fd7", "#ff5fff",
    "#ff8700", "#ff875f", "#ff8787", "#ff87af", "#ff87d7", "#ff87ff", "#ffaf00", "#ffaf5f",
    "#ffaf87", "#ffafaf", "#ffafd7", "#ffafff", "#ffd700", "#ffd75f", "#ffd787", "#ffd7af",
    "#ffd7d7", "#ffd7ff", "#ffff00", "#ffff5f", "#ffff87", "#ffffaf", "#ffffd7", "#ffffff",
    "#080808", "#121212", "#1c1c1c", "#262626", "#303030", "#3a3a3a", "#444444", "#4e4e4e",
    "#585858", "#626262", "#6c6c6c", "#767676", "#808080", "#8a8a8a", "#949494", "#9e9e9e",
    "#a8a8a8", "#b2b2b2", "#bcbcbc", "#c6c6c6", "#d0d0d0", "#dadada", "#e4e4e4", "#eeeeee"
]
# fmt: on


def increase_saturation(rgb: list[int], factor=10) -> list[int]:
    r, g, b = [x / 255.0 for x in rgb]  # Normalize to 0-1
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # Convert to HLS
    s = min(1, s * factor)  # Boost saturation
    r, g, b = colorsys.hls_to_rgb(h, l, s)  # Convert back to RGB
    return tuple(int(x * 255) for x in (r, g, b))


def hex2rgb(hex: str) -> list[int]:
    if hex[0] == "#":
        hex = hex[1:]  # strip leading '#' if it exists
    assert isinstance(hex, str) and (len(hex) == 6), "string of length 6 is required!"
    r_str, g_str, b_str = hex[:2], hex[2:4], hex[4:]
    return [int(x, 16) for x in [r_str, g_str, b_str]]


def rgb2hex(rgb: list[int]) -> str:
    return "#" + "".join([hex(x)[2:].zfill(2) for x in rgb])


def color_distance(rgb1, rgb2):
    "calculate Euclidean distance between two RGB colors"
    return sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)))


def format_rgb_escape_code_colored(rgb: list[int], reverse=False) -> None:
    """
    print rgb value as hex code styled using ANSI escape sequences
    uses black or white background depending on brightness
    """
    bold = "\033[1m"
    reverse_or_empty = "\033[7m" if reverse else ""
    if sum(rgb) < ((255 * 3) / 2):  # if less than 50% brightness
        white_background = "\033[48;2;255;255;255m"
        return f"{white_background}{bold}\033[38;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m{reverse_or_empty}{rgb2hex(rgb)}\033[0m"
    black_background = "\033[48;2;0;0;0m"
    return f"{black_background}{bold}\033[38;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m{reverse_or_empty}{rgb2hex(rgb)}\033[0m"


def find_closest_discord_color(
    rgb: list[int], sequence_1st_number: int, do_increase_saturation=True
):
    if do_increase_saturation:
        rgb = increase_saturation(rgb)
    if sequence_1st_number == 38:
        hex_to_4bit_index = DISCORD_FG_HEX_TO_4BIT_INDEX
        fg_or_bg = "foreground"
        reverse = False
        # light colors tend to become white, so we made all other colors preferred unless the
        # input color is *really* white (RGB all > 200)
        if all(num > 200 for num in rgb):
            return 37
    elif sequence_1st_number == 48:
        hex_to_4bit_index = DISCORD_BG_HEX_TO_4BIT_INDEX
        fg_or_bg = "background"
        reverse = True
    else:
        raise RuntimeError(f"expected sequence 1st number of 38 or 48, got {sequence_1st_number}")
    sorted_discord_hex = sorted(
        hex_to_4bit_index.keys(),
        key=lambda discord_hex: color_distance(hex2rgb(discord_hex), rgb),
    )
    if DEBUG:
        sorted_discord_rgb = [hex2rgb(x) for x in sorted_discord_hex]
        print(
            f"closest {fg_or_bg} to {format_rgb_escape_code_colored(rgb, reverse=reverse)}: {", ".join([format_rgb_escape_code_colored(x, reverse=reverse) for x in sorted_discord_rgb])}",
            file=sys.stderr,
        )
    return hex_to_4bit_index[sorted_discord_hex[0]]


def process_sequence_numbers(sequence_numbers: list[int]) -> list[int]:
    if len(sequence_numbers) == 0:  # empty sequence implies reset
        return [0]

    if len(sequence_numbers) == 1:  # 4 bit formatting OR color
        if sequence_numbers[0] not in [0, 1, 4] + (list(range(30, 38)) + list(range(40, 48))):
            print(f"invalid 1 digit sequence: {sequence_numbers}", file=sys.stderr)
        return sequence_numbers

    if len(sequence_numbers) == 2:  # 4 bit formatting AND color
        if sequence_numbers[0] not in [0, 1, 4]:
            print(f"invalid 2 digit sequence 1st num: {sequence_numbers[0]}", file=sys.stderr)
        if sequence_numbers[1] not in (list(range(30, 38)) + list(range(40, 48))):
            print(f"invalid 2 digit sequence 2nd num: {sequence_numbers[1]}", file=sys.stderr)
        return sequence_numbers

    if len(sequence_numbers) == 3:  # 8 bit color
        if sequence_numbers[0] not in [38, 48]:
            print(f"invalid 3 digit sequence 1st num: {sequence_numbers[0]}", file=sys.stderr)
        if sequence_numbers[1] != 5:
            print(f"invalid 3 digit sequence 2nd num: {sequence_numbers[1]}", file=sys.stderr)
        color_index = sequence_numbers[2]
        return [
            sequence_numbers[0],
            5,
            find_closest_discord_color(
                hex2rgb(FAKE_8BIT_INDEX_TO_HEX[color_index]), sequence_numbers[0]
            ),
        ]

    if len(sequence_numbers) == 5:  # 24 bit color
        if sequence_numbers[0] not in [38, 48]:
            print(f"invalid 5 digit sequence 1st num: {sequence_numbers[0]}", file=sys.stderr)
        if sequence_numbers[1] != 2:
            print(f"invalid 5 digit sequence 2nd num: {sequence_numbers[1]}", file=sys.stderr)
        return [
            sequence_numbers[0],
            2,
            find_closest_discord_color(sequence_numbers[2:], sequence_numbers[0]),
        ]

    raise RuntimeError(f"too many numbers in sequence: {sequence_numbers}")


chunks = re.split(ANSI_ESCAPE_8BIT, sys.stdin.read())
message_chunks = []
for chunk in chunks:
    if not re.match(ANSI_ESCAPE_8BIT, chunk):
        message_chunks.append(chunk)
        continue
    sequence = chunk[2:]  # remove '\x1b['
    sequence = sequence[:-1]  # remove 'm'
    sequence_numbers = []
    for sequence_number_str in sequence.split(";"):
        try:
            sequence_numbers.append(int(sequence_number_str))
        except ValueError:
            if sequence_number_str == "":
                sequence_numbers.append(0)  # default 0 for empty number
            else:
                print(f"invalid sequence number string: {sequence_number_str}")
    new_numbers = process_sequence_numbers(sequence_numbers)
    new_numbers_str = [str(x) for x in new_numbers]
    message_chunks.append(f"\033[{";".join(new_numbers_str)}m")

print("".join(message_chunks))
