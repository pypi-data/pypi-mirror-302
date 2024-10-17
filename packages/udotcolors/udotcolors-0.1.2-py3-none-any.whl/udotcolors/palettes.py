from .colors import get_color_list
import pprint


_palettes = {
    "qualitative": {
        "main": get_color_list(
            "light_blue",
            "orange",
            "dark_blue",
            "gray",
            "medium_blue",
            "light_green",
            "dark_gray",
            "turquoise",
            "tacao",
            "brown",
        ),
        "alt": get_color_list(),
        "grayscale": get_color_list(),
        "highlight": get_color_list(),
    },
    "sequential": {
        "blue": get_color_list("darkblue", "white"),
    },
    "diverging": {
        "blueorange": get_color_list("blue", "orange"),
    },
}


def list_palettes():
    pprint.pprint(_palettes)
    return None


def get_palette_qual(palette="main"):
    palette = _sanitize_palette_name(palette)
    return _palettes["qualitative"][palette]


get_palette = get_palette_qual


def get_palette_seq(palette="blue"):
    palette = _sanitize_palette_name(palette)
    return _palettes["sequential"][palette]


def get_palette_div(palette="blueorange"):
    palette = _sanitize_palette_name(palette)
    return _palettes["diverging"][palette]


def _sanitize_palette_name(pal: str) -> str:
    pal = pal.lower().replace("grey", "gray").replace("_", "")
    return pal
