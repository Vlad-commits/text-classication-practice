# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import numpy as np

import ml_model
import utils
import dataframe_provider
import plots_utils
from utils import save_test_report_to_tex

df = dataframe_provider.get_dataframe()


# no cv c = 1
def simple_case(columns, saveplots=False):
    print("Train model using " + str(columns) + " features and C=1")

    x = df[columns].to_numpy()
    y = df["author_label"].to_numpy()

    x_train, x_test, y_train, y_test = utils.split(x, y)

    model = ml_model.Model(c=1)
    (w, b) = model.fit(x_train, y_train)

    predicted_train = model.predict(x_train)
    predicted_test = model.predict(x_test)
    print("w: (%0.2f,%0.2f) b: %0.2f" % (w[0], w[1], b))
    utils.print_reports(y_train, predicted_train, y_test, predicted_test)

    if not saveplots:
        file = None
    else:
        file = columns[0] + "_" + columns[1]
        report_file_tex = "./report/tables/test_report_" + columns[0] + "_" + columns[1] + ".tex"
        save_test_report_to_tex(y_test, predicted_test, file=report_file_tex)
    plots_utils.classification_plot(w, b,
                                    x1=x[y == 1],
                                    x2=x[y == -1],
                                    labels=["Chekhov", "Kuprin"],
                                    axis_labels=columns,
                                    transformation_function=lambda x: model.transform_features(x),
                                    reverse_trasformation_function=lambda x: model.reverse_transform(x),
                                    file=file)
    return utils.cross_validate_accuracy(x, y)


# Choose c
def with_choosing_c_param(columns, saveplots=False):
    print("Train model using " + str(columns) + " features and using cross-validation to choose C :")

    x = df[columns].to_numpy()
    y = df["author_label"].to_numpy()
    x_train, x_test, y_train, y_test = utils.split(x, y)

    c, scores = utils.cross_validate_and_choose_c(x_train, y_train)
    print("Best c is: %f" % c)

    model = ml_model.Model(c)
    (w, b) = model.fit(x_train, y_train)

    predicted_train = model.predict(x_train)
    predicted_test = model.predict(x_test)

    utils.print_reports(y_train, predicted_train, y_test, predicted_test)

    if not saveplots:
        file = None
    else:
        file = "choosing_C_" + columns[0] + "_" + columns[1]
        report_tex_file = "./report/tables/test_report_CV" + columns[0] + "_" + columns[1] + ".tex"
        save_test_report_to_tex(y_test, predicted_test, file=report_tex_file)
    plots_utils.classification_plot(w, b,
                                    x1=x[y == 1],
                                    x2=x[y == -1],
                                    labels=["Chekhov", "Kuprin"],
                                    axis_labels=columns,
                                    transformation_function=lambda x: model.transform_features(x),
                                    reverse_trasformation_function=lambda x: model.reverse_transform(x),
                                    file=file)
    return utils.cross_validate_accuracy(x, y, True, c)


def with_svd(saveplots=False):
    print("Train model using PCA to select 2 features and using cross-validation to choose C :")

    x = df[df.columns.difference(["author_label"])].to_numpy()
    y = df["author_label"].to_numpy()
    x_train, x_test, y_train, y_test = utils.split(x, y)

    c, scores_dict = utils.cross_validate_and_choose_c(x_train, y_train, True)
    print("Best c is: %f" % c)

    model = ml_model.Model(c, use_svd=True)
    (w, b) = model.fit(x_train, y_train)

    predicted_train = model.predict(x_train)
    predicted_test = model.predict(x_test)

    utils.print_reports(y_train, predicted_train, y_test, predicted_test)

    np.set_printoptions(precision=3)
    print("Features transformation matrix:")
    print(model.transformation_matrix)

    if not saveplots:
        file = None
    else:
        file = "with_PCA"
        save_test_report_to_tex(y_test, model.predict(x_test),
                                "./report/tables/test_report_svd.tex")

    plots_utils.classification_plot(w, b,
                                    x1=x[y == 1],
                                    x2=x[y == -1],
                                    labels=["Chekhov", "Kuprin"],
                                    axis_labels=["Projection on first PC", "Projection on second PC"],
                                    transformation_function=lambda x: model.transform_features(x),
                                    reverse_trasformation_function=lambda x: model.reverse_transform(x),
                                    file=file,
                                    plot_original=False)
    return utils.cross_validate_accuracy(x, y, True, c)


def main():
    simple_case(["letters_count", "total_punctuation_signs"], False)
    plt.show()


if __name__ == '__main__':
    main()
