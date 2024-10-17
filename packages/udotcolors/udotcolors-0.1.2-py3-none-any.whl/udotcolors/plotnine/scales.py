import plotnine
from .palettes import _palette_gen, _palette_gen_seq, _palette_gen_div

## Discrete scales ####


def scale_fill_udot(
    palette="main",
    reverse=False,
    # backward=False,
    **kwargs,
):
    scale = plotnine.scales.scale_discrete.scale_discrete(
        aesthetics="fill",
        palette=_palette_gen(
            palette=palette,
            reverse=reverse,
            # backward=backward,
        ),
        **kwargs,
    )
    return scale


def scale_color_udot(
    palette="main",
    reverse=False,
    # backward=False,
    **kwargs,
):
    scale = plotnine.scales.scale_discrete.scale_discrete(
        aesthetics="color",
        palette=_palette_gen(
            palette=palette,
            reverse=reverse,
            # backward=backward,
        ),
        **kwargs,
    )
    return scale


scale_colour_udot = scale_color_udot


## Sequential scales ####


def scale_fill_udot_seq(
    palette=None,
    colorlist=None,
    reverse=False,
    **kwargs,
):
    colordict = _palette_gen_seq(palette=palette, colorlist=colorlist, reverse=reverse)
    scale = plotnine.scale_fill_gradientn(
        colors=colordict["colors"], values=colordict["values"], **kwargs
    )
    return scale


def scale_color_udot_seq(
    palette=None,
    colorlist=None,
    reverse=False,
    **kwargs,
):
    colordict = _palette_gen_seq(palette=palette, colorlist=colorlist, reverse=reverse)
    scale = plotnine.scale_color_gradientn(
        colors=colordict["colors"], values=colordict["values"], **kwargs
    )
    return scale


scale_colour_udot_seq = scale_color_udot_seq


## Diverging scales


def scale_fill_udot_div(
    palette=None,
    colors=None,
    midpoint=0,
    reverse=False,
    **kwargs,
):
    colordict = _palette_gen_div(palette=palette, colors=colors, reverse=reverse)
    scale = plotnine.scale_fill_gradient2(
        low=colordict["low"],
        mid=colordict["mid"],
        high=colordict["high"],
        midpoint=midpoint,
        **kwargs,
    )
    return scale


def scale_color_udot_div(
    palette=None,
    colors=None,
    midpoint=0,
    reverse=False,
    **kwargs,
):
    colordict = _palette_gen_div(palette=palette, colors=colors, reverse=reverse)
    scale = plotnine.scale_color_gradient2(
        low=colordict["low"],
        mid=colordict["mid"],
        high=colordict["high"],
        midpoint=midpoint,
        **kwargs,
    )
    return scale


scale_colour_udot_div = scale_color_udot_div
