import pprint

_primary = {
    "lightblue": "#5A87C6",
    "orange": "#E86924",
    "darkblue": "#0B2444",
}
_secondary = {
    "lightgreen": "#ABC746",
    "mustard": "#F5A31B",
    "mediumblue": "#09549C",
    "tan": "#C7A25A",
    "turquoise": "#55CCD4",
    "red": "#E8261A",  # Only use to highlight something strong or negative
}
_tertiary = {
    "redrock": "#C7776D",
    "brown": "#7A5B1F",
    "tacao": "#F7AA74",
    "purple": "#8A52A1",
    "darkgreen": "#6B7A31",
    "yellow": "#DED843",
}
_grays = {
    "black": "#000000",
    "darkgray": "#454545",
    "gray": "#888888",
    "lightgray": "#EEEEEE",
    "white": "#FFFFFF",
}

_udot_colors_dict = {
    "primary": _primary,
    "secondary": _secondary,
    "tertiary": _tertiary,
    "grays": _grays,
}


def get_color(col):
    all_colors = _primary | _secondary | _tertiary | _grays
    col = _sanitize_color_name(col)
    return all_colors[col]


def get_color_list(*cols):
    all_colors = _primary | _secondary | _tertiary | _grays
    cols = [_sanitize_color_name(c) for c in cols]
    return [all_colors[c] for c in cols]


def get_color_category(*cols):
    cols = [_sanitize_color_name(c) for c in cols]
    return [_udot_colors_dict[c] for c in cols]


def list_colors(*cols):
    red_msg = "Only use red to highlight something strong or negative"
    if len(cols) < 1:
        pprint.pprint(red_msg)
        pprint.pprint(_udot_colors_dict)
    else:
        if any([c == "secondary" for c in cols]):
            print(red_msg)
        for c in cols:
            c = _sanitize_color_name(c)
            print(c + ":")
            pprint.pprint(_udot_colors_dict[c])


def _sanitize_color_name(col: str) -> str:
    col = col.lower().replace("grey", "gray").replace("_", "")
    col = "mediumblue" if col == "blue" else col
    col = "darkgreen" if col == "green" else col
    return col
