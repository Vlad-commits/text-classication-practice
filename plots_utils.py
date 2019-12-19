# -*- coding: utf-8 -*-
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def classification_plot(w, b, x1, x2, labels, axis_labels, transformation_function,
                        reverse_trasformation_function, file=None, plot_original=True):
    if file is not None:
        matplotlib.use("pgf")
        matplotlib.rcParams.update({
            "pgf.texsystem": "pdflatex",
            # 'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
            "pgf.preamble": [
                r"\usepackage[utf8]{inputenc}",
                r"\usepackage[T1]{fontenc}",
                r"\usepackage{cmbright}",
            ]
        })

    if file is not None or not plot_original:
        fig, ax = plt.subplots()
        ax.margins(0.05)
        x1_t = transformation_function(x1)
        x2_t = transformation_function(x2)
        ax.plot(x1_t[:, 0], x1_t[:, 1], marker='o', linestyle='', ms=2, label=labels[0])
        ax.plot(x2_t[:, 0], x2_t[:, 1], marker='o', linestyle='', ms=2, label=labels[1])
        ax.legend()
        ax.set_xlabel(axis_labels[0])
        ax.set_ylabel(axis_labels[1])

        if file is not None:
            plt.savefig(os.path.abspath("./report/fig/" + file + "_1.pgf"))
        linexs = np.linspace(min(x1_t[:, 0].min(), x2_t[:, 0].min()), max(x1_t[:, 0].max(), x2_t[:, 0].max()))
        line = [(-w[0] * x + b) / w[1] for x in linexs]
        plt.plot(linexs, line)

        if file is not None:
            plt.savefig(os.path.abspath("./report/fig/" + file + "_2.pgf"))


    if plot_original:
        fig, ax = plt.subplots()
        ax.margins(0.05)

        ax.plot(x1[:, 0], x1[:, 1], marker='o', linestyle='', ms=2, label=labels[0])
        ax.plot(x2[:, 0], x2[:, 1], marker='o', linestyle='', ms=2, label=labels[1])
        ax.legend()
        ax.set_xlabel(axis_labels[0])
        ax.set_ylabel(axis_labels[1])

        if file is not None:
            plt.savefig(os.path.abspath("./report/fig/" + file + "_0.pgf"))

        x1_t = transformation_function(x1)
        x2_t = transformation_function(x2)
        linexs = np.linspace(min(x1_t[:, 0].min(), x2_t[:, 0].min()), max(x1_t[:, 0].max(), x2_t[:, 0].max()))
        tranformed_line = reverse_trasformation_function([[x, (-w[0] * x + b) / w[1]] for x in linexs])
        plt.plot(tranformed_line[:, 0], tranformed_line[:, 1])

        if file is not None:
            plt.savefig(os.path.abspath("./report/fig/" + file + "_4.pgf"))
