"""Shared chart styling so every figure in the notebook reads as one system."""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

SURFACE = "#fcfcfb"
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED_INK = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

# Categorical slots, fixed order — never reassigned per-chart.
SERIES_1 = "#2a78d6"  # blue   — primary series (actual / history)
SERIES_2 = "#1baf7a"  # aqua   — secondary series (predicted / forecast)
SERIES_2_BAND = "#9ec5f4"  # light blue — RMSE band fill (sequential step, not a new hue)


def apply_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "axes.edgecolor": BASELINE,
            "axes.labelcolor": SECONDARY_INK,
            "axes.titlecolor": PRIMARY_INK,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.color": GRIDLINE,
            "grid.linewidth": 0.8,
            "xtick.color": MUTED_INK,
            "ytick.color": MUTED_INK,
            "text.color": PRIMARY_INK,
            "font.family": "sans-serif",
            "font.size": 10.5,
            "lines.linewidth": 2.0,
            "lines.solid_capstyle": "round",
            "figure.dpi": 110,
            "savefig.dpi": 150,
        }
    )


def currency_axis(ax, axis: str = "y") -> None:
    formatter = mticker.FuncFormatter(lambda x, _pos: f"£{x:,.0f}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(formatter)
