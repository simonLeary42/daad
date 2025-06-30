#!/bin/env python3
import re
import sys
from math import sqrt
import colorsys

DEBUG = False

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
    # "FFFFFF": 37, # white is a special case, see below
}

DISCORD_BG_HEX_TO_4BIT_INDEX = {
    "022029": 40,  # firefly dark blue
    "BD3612": 41,  # orange
    "475B62": 42,  # marble blue
    "536870": 43,  # greyish turquoise
    "708285": 44,  # gray
    "595AB7": 45,  # indigo
    "819090": 46,  # light gray
    # "FCF4DC": 47,  # white is a special case, see below
}

# these colors are customizable by a terminal emulator, so we must assume a reasonable default
FAKE_4BIT_FG_INDEX_TO_HEX = {}
FAKE_4BIT_BG_INDEX_TO_HEX = {}
RELATIVE_4BIT_INDEX_TO_HEX = {
    0: "000000",  # black
    1: "B83019",  # red
    2: "51BF37",  # green
    3: "C6C43D",  # yellow
    4: "0C24BF",  # blue
    5: "B93EC1",  # magenta
    6: "53C2C5",  # cyan
    7: "FFFFFF",  # white
}
for x in 30, 90:  # 30 is foreground color, 90 is same + high intensity
    for offset, _hex in RELATIVE_4BIT_INDEX_TO_HEX.items():
        FAKE_4BIT_FG_INDEX_TO_HEX[x + offset] = _hex
for x in 40, 100:  # 40 is background color, 100 is same + high intensity
    for offset, _hex in RELATIVE_4BIT_INDEX_TO_HEX.items():
        FAKE_4BIT_BG_INDEX_TO_HEX[x + offset] = _hex
VALID_4BIT_FG_INDEXES = list(FAKE_4BIT_FG_INDEX_TO_HEX.keys())
VALID_4BIT_BG_INDEXES = list(FAKE_4BIT_BG_INDEX_TO_HEX.keys())
VALID_4BIT_INDEXES = VALID_4BIT_FG_INDEXES + VALID_4BIT_BG_INDEXES

# in this case, "format index" is a CSR parameter which is not color
# discord only supports reset, bold, underline
# 21 (end bold) and 24 (end underline) do not work as of 2025/6/29
# TODO find a better word than "index"
SUPPORTED_FORMAT_INDEXES = [0, 1, 4]

# these colors are customizable by a terminal emulator, so we must assume a reasonable default
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


class InvalidSequenceError(Exception):
    pass


def increase_saturation(rgb: list[int], factor=10) -> list[int]:
    r, g, b = [x / 255.0 for x in rgb]  # Normalize to 0-1
    h, l, s = colorsys.rgb_to_hls(r, g, b)  # Convert to HLS
    s = min(1, s * factor)  # Boost saturation
    r, g, b = colorsys.hls_to_rgb(h, l, s)  # Convert back to RGB
    return tuple(int(x * 255) for x in (r, g, b))


def hex2rgb(_hex: str) -> list[int]:
    if _hex[0] == "#":
        _hex = _hex[1:]  # strip leading '#' if it exists
    assert isinstance(_hex, str) and (len(_hex) == 6), "string of length 6 is required!"
    r_str, g_str, b_str = _hex[:2], _hex[2:4], _hex[4:]
    return [int(x, 16) for x in [r_str, g_str, b_str]]


def rgb2hex(rgb: list[int]) -> str:
    return "#" + "".join([hex(x)[2:].zfill(2) for x in rgb])


def color_distance(rgb1, rgb2):
    "calculate Euclidean distance between two RGB colors"
    return sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)))


def format_rgb_escape_code_colored(rgb: list[int]) -> None:
    """
    print rgb value as hex code styled using ANSI escape sequences
    uses black or white background depending on brightness
    for debugging purposes
    """
    bold = "\033[1m"
    if sum(rgb) < ((255 * 3) / 2):  # if less than 50% brightness
        white_foreground = "\033[38;2;255;255;255m"
        return f"{white_foreground}{bold}\033[48;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m{rgb2hex(rgb)}\033[0m"
    black_foreground = "\033[38;2;0;0;0m"
    return f"{black_foreground}{bold}\033[48;2;{str(rgb[0])};{str(rgb[1])};{str(rgb[2])}m{rgb2hex(rgb)}\033[0m"


def find_closest_discord_color(rgb: list[int], fg_or_bg: str, do_increase_saturation=True) -> int:
    if do_increase_saturation:
        rgb = increase_saturation(rgb)
    if fg_or_bg == "foreground":
        hex_to_4bit_index = DISCORD_FG_HEX_TO_4BIT_INDEX
        # light colors tend to become white, so we made all other colors preferred unless the
        # input color is *really* white (RGB all > 200)
        if all(num > 200 for num in rgb):
            return 37
    elif fg_or_bg == "background":
        hex_to_4bit_index = DISCORD_BG_HEX_TO_4BIT_INDEX
        # light colors tend to become white, so we made all other colors preferred unless the
        # input color is *really* white (RGB all > 200)
        if all(num > 200 for num in rgb):
            return 47
    else:
        raise RuntimeError(f"neither 'foreground' nor 'background': '{fg_or_bg}'")
    sorted_discord_hex = sorted(
        hex_to_4bit_index.keys(),
        key=lambda discord_hex: color_distance(hex2rgb(discord_hex), rgb),
    )
    if DEBUG:
        # fmt: off
        print(
            "closest %s to %s: %s" % (
                fg_or_bg,
                format_rgb_escape_code_colored(rgb),
                ", ".join([format_rgb_escape_code_colored(hex2rgb(x)) for x in sorted_discord_hex])
            ),
            file=sys.stderr,
        )
        # fmt: on
    return hex_to_4bit_index[sorted_discord_hex[0]]


def join_sequence(sequence: list[int]) -> str:
    return "\x1b[" + ";".join([str(x) for x in sequence]) + "m"


def process_sequence(sequence: str) -> str:
    sequence = sequence[2:]  # remove '\x1b['
    sequence = sequence[:-1]  # remove 'm'
    sequence = sequence.split(";")
    # special case: 0;38:2:x:r:g:b;48:2:x:r:g:b (not sure what x is so I ignore it)
    if (
        len(sequence) == 3
        and sequence[0] == "0"
        and sequence[1].startswith("38:2:")
        and sequence[2].startswith("48:2:")
    ):
        try:
            fg_rgb = [int(x) for x in sequence[1].split(":")[-3:]]
            bg_rgb = [int(x) for x in sequence[2].split(":")[-3:]]
        except ValueError as e:
            raise InvalidSequenceError(sequence) from e
        return "%s%s" % (
            join_sequence(_process_sequence([38, 2] + fg_rgb)),
            join_sequence(_process_sequence([48, 2] + bg_rgb)),
        )
    # special case: 0;38:2:x:r:g:b (not sure what x is so I ignore it)
    if len(sequence) == 2 and sequence[0] == "0" and sequence[1].startswith("38:2:"):
        try:
            rgb = [int(x) for x in sequence[1].split(":")[-3:]]
        except ValueError as e:
            raise InvalidSequenceError(sequence) from e
        return join_sequence(_process_sequence([38, 2] + rgb))
    # special case: 0;48:2:x:r:g:b (not sure what x is so I ignore it)
    if len(sequence) == 2 and sequence[0] == "0" and sequence[1].startswith("48:2:"):
        try:
            rgb = [int(x) for x in sequence[1].split(":")[-3:]]
        except ValueError as e:
            raise InvalidSequenceError(sequence) from e
        return join_sequence(_process_sequence([48, 2] + rgb))
    # cast to int
    try:
        sequence = [int(x) for x in sequence]
    except ValueError:
        raise InvalidSequenceError(sequence) from e
    # special case 1;31;41 (4 bit formatting and foreground and background)
    if (
        len(sequence) == 3
        and sequence[1] in VALID_4BIT_INDEXES
        and sequence[2] in VALID_4BIT_INDEXES
    ):
        return "%s%s" % (
            join_sequence(_process_sequence([sequence[0], sequence[1]])),
            join_sequence(_process_sequence([sequence[0], sequence[2]])),
        )
    # special case: 31 (4 bit color with no leading formatting)
    if (len(sequence) == 1) and (sequence[0] in VALID_4BIT_INDEXES):
        return join_sequence(_process_sequence([0, sequence[0]]))
    # normal case
    return join_sequence(_process_sequence(sequence))


def _process_sequence(sequence_numbers: list[int]) -> list[int]:
    # input sequence can be 1, 2, 3, or 5 numbers
    # output sequence can be 1 or 2 numbers

    if len(sequence_numbers) == 1:  # 4 bit formatting
        if sequence_numbers[0] not in SUPPORTED_FORMAT_INDEXES:
            # can't substitute with 0 because that would reset all formatting
            raise InvalidSequenceError(f"invalid 1 digit sequence: [{sequence_numbers[0]}]")
        return sequence_numbers

    if len(sequence_numbers) == 2:  # 4 bit formatting and color
        formatting, color_index = sequence_numbers
        if formatting not in SUPPORTED_FORMAT_INDEXES:
            # can substitute with 0 because it has no effect when followed with a color
            print(
                f"ignoring unsupported 1st number of sequence: {sequence_numbers[0]}",
                file=sys.stderr,
            )
            formatting = 0
        if color_index in VALID_4BIT_FG_INDEXES:
            return [
                formatting,
                find_closest_discord_color(
                    hex2rgb(FAKE_4BIT_FG_INDEX_TO_HEX[color_index]), "foreground"
                ),
            ]
        if color_index in VALID_4BIT_BG_INDEXES:
            return [
                formatting,
                find_closest_discord_color(
                    hex2rgb(FAKE_4BIT_BG_INDEX_TO_HEX[color_index]), "background"
                ),
            ]
        raise InvalidSequenceError(f"invalid 2 digit sequence 2nd num: {sequence_numbers[1]}")

    if len(sequence_numbers) == 3:  # 8 bit color
        if sequence_numbers[0] not in [38, 48]:
            raise InvalidSequenceError(f"invalid 3 digit sequence 1st num: {sequence_numbers[0]}")
        if sequence_numbers[1] != 5:
            raise InvalidSequenceError(f"invalid 3 digit sequence 2nd num: {sequence_numbers[1]}")
        color_index = sequence_numbers[2]
        return [
            find_closest_discord_color(
                hex2rgb(FAKE_8BIT_INDEX_TO_HEX[color_index]),
                "foreground" if sequence_numbers[0] == 38 else "background",
            ),
        ]

    if len(sequence_numbers) == 5:  # 24 bit color
        if sequence_numbers[0] not in [38, 48]:
            raise InvalidSequenceError(f"invalid 5 digit sequence 1st num: {sequence_numbers[0]}")
        if sequence_numbers[1] != 2:
            raise InvalidSequenceError("invalid 5 digit sequence 2nd num: {sequence_numbers[1]}")
        return [
            find_closest_discord_color(
                sequence_numbers[2:],
                "foreground" if sequence_numbers[0] == 38 else "background",
            )
        ]

    raise InvalidSequenceError(f"sequence length is not 1, 2, 3, or 5: {sequence_numbers}")


chunks = re.split(ANSI_ESCAPE_8BIT, sys.stdin.read())
for chunk in chunks:
    if (not re.match(ANSI_ESCAPE_8BIT, chunk)) or chunk == "\x1b[m":
        print(chunk, end="")
    else:
        try:
            print(process_sequence(chunk), end="")
        except InvalidSequenceError as e:
            print(e, file=sys.stderr)
