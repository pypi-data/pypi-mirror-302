# %%
from udotcolors.plotnine.scales import *
from plotnine import *
from plotnine.data import mtcars

# %%
mtcars2 = mtcars.assign(gear=[str(x) for x in mtcars.gear])

# %%
(
    ggplot(mtcars2, aes(x="cyl", y="mpg", color="gear"))
    + geom_point()
    + scale_color_udot()
)

# %%
(
    ggplot(mtcars2, aes(x="cyl", y="mpg", color="name"))
    + geom_point()
    + scale_color_udot()
)

# %%
(
    ggplot(mtcars, aes(x="cyl", y="mpg", fill="gear"))
    + geom_col()
    + scale_fill_udot_seq(colorlist=[("white", 0), ("blue", 1)])
)

# %%
(
    ggplot(mtcars, aes(x="cyl", y="mpg", fill="gear"))
    + geom_col()
    + scale_fill_udot_div(colors=["blue", "orange"], midpoint=4)
)

# %%
(
    ggplot(mtcars, aes(x="cyl", y="mpg", fill="gear"))
    + geom_col()
    + scale_fill_udot_seq("blue", reverse=True)
)
