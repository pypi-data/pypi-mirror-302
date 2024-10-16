import pathlib

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import font_manager


def load_logo_font(family="Quicksand"):
    this_folder = pathlib.Path(__file__).parent
    path_to_fonts = this_folder / "fonts" / family / "static"
    for font in path_to_fonts.glob("*.ttf"):
        font_manager.fontManager.addfont(str(font))
    mpl.rc("font", family=family)


def logoize(words, dest, light=True, format="svg"):
    color = (0.0, 0.0, 0.0) if light else (1.0, 1.0, 1.0)
    load_logo_font()

    plt.figtext(
        0.5,
        0.5,
        words,
        size=500,
        ha="center",
        va="center",
        fontweight="bold",
        color=color,
    )
    plt.savefig(dest, bbox_inches="tight", transparent=True, format=format)
