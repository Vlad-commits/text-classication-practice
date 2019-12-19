import math
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import argmin

np.random.seed(42)
n = 50

a = -1
b = 30

xs_1 = 25 * np.random.random_sample(n)
ys_1 = (b + a * xs_1) * np.random.random_sample(n) - (b / 10) + (b / 20) * np.random.random_sample(n)

xs_2 = 25 * np.random.random_sample(n) + 5
ys_2 = (30 - (b + a * xs_2)) * np.random.random_sample(n) + (b + a * xs_2) * 1.05 + (b / 10) - (
        b / 20) * np.random.random_sample(n)


# ax.set_autoscale_on(False)
# ax.set_autoscaley_on(False)
# ax.set_autoscalex_on(False)
#
# ax.set_ylim([0,30])
# ax.set_xlim([0,30])
# ax.set_xmargin(0)
# ax.set_ymargin(0)
#
# ax.autoscale_view()


def plot_scatter(ax, fig1):
    ax.plot(xs_1, ys_1, marker='o', linestyle='', ms=2, label="$y=1$")

    ax.plot(xs_2, ys_2, marker='o', linestyle='', ms=2, label="$y= -1$")

    linexs = np.linspace(0, 30)
    line = [- x + b for x in linexs]

    ax.plot(linexs, line, label="$\mathbf{w}^{T} \mathbf{x}-b=0$")

    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")

    ax.set_xticks([])
    ax.set_yticks([])

    ax.legend()
    ax.axis('equal')


def plot_lowest_margins(ax, fig):
    closet_1 = int(argmin([abs((xs_1[i] + ys_1[i] - b)) for i in range(len(xs_1))]))
    range_1 = min([abs((xs_1[i] + ys_1[i] - b)) for i in range(len(xs_1))])
    closet_2 = int(argmin([abs((xs_2[i] + ys_2[i] - b)) for i in range(len(xs_2))]))
    range_2 = min([abs((xs_2[i] + ys_2[i] - b)) for i in range(len(xs_2))])

    ax.plot([xs_1[closet_1], xs_1[closet_1] + range_1 / 2],
             [ys_1[closet_1], ys_1[closet_1] + range_1 / 2])
    ax.plot([xs_2[closet_2], xs_2[closet_2] - range_2 / 2],
             [ys_2[closet_2], ys_2[closet_2] - range_2 / 2])


# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     # 'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
#     "pgf.preamble": [
#         r"\usepackage[utf8x]{inputenc}",
#         r"\usepackage[T1]{fontenc}",
#         r"\usepackage{cmbright}",
#     ]
# })


def plot_line(ax, fig):
    if True:
        linexs = np.linspace(0, 30)
        line = [- 0.95 * x + b + 1 for x in linexs]
        ax.plot(linexs, line, label="$\mathbf{w}_1^{T} \mathbf{x}-b_1=0$")
    if True:
        linexs = np.linspace(0, 30)
        line = [- 1.1 * x + b - 1 for x in linexs]
        ax.plot(linexs, line, label="$\mathbf{w}_2^{T} \mathbf{x}-b_2=0$")
    ax.legend()







def save():
    matplotlib.use("pgf")
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        # 'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
        "pgf.preamble": [
            r"\usepackage[utf8x]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{cmbright}",
        ]
    })
    fig1, ax1 = plt.subplots()
    plot_scatter(ax1, fig1)

    plt.savefig(os.path.abspath("./report/fig/example1.pgf"))

    plot_lowest_margins(ax1, fig1)
    plt.savefig(os.path.abspath("./report/fig/example2.pgf"))

    fig2, ax2 = plt.subplots()
    plot_scatter(ax2, fig2)
    plot_line(ax2, fig2)
    plt.savefig(os.path.abspath("./report/fig/example3.pgf"))


def show():
    fig1, ax1 = plt.subplots()
    plot_scatter(ax1, fig1)
    plot_lowest_margins(ax1, fig1)

    fig2, ax2 = plt.subplots()
    plot_scatter(ax2, fig2)
    plot_line(ax2, fig2)

    plt.show()



save()
# show()
