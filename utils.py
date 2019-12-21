import sklearn
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_validate, RepeatedStratifiedKFold

import ml_model


def split(X, y):
    return sklearn.model_selection.train_test_split(X, y, test_size=0.3, random_state=4243, stratify=y)


def cross_validate_accuracy(X_train, y_train, use_svd=False, c=1):
    model = ml_model.Model(c, use_svd)
    n_splits = 10
    cv_strategy = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=2, random_state=42)
    cvs = cross_validate(model, X_train, y_train, cv=cv_strategy,
                         scoring=['accuracy', 'precision_macro', 'precision_weighted'])
    cv_scores = cvs['test_precision_macro']

    return cv_scores


def cross_validate_and_choose_c(X, y, use_svd=False, cs=None):
    if cs is None:
        cs = [0.1, 1, 10, 100, 1000, 5000,10000]

    c = cs[0]
    best_c = c
    best_scores = cross_validate_accuracy(X, y, use_svd, c)
    print("For c=%f minimal accuracy: %0.2f " % (c, best_scores.min()))

    scoress_dict = {}
    for c in cs[1:]:
        scores = cross_validate_accuracy(X, y, use_svd, c)
        scoress_dict[c] = scores
        print("For c=%f minimal accuracy: %0.2f " % (c, scores.min()))
        if scores.min() > best_scores.min():
            best_scores = scores
            best_c = c

    return best_c, scoress_dict


def print_reports(y_train=None, predicted_train=None, y_test=None, predicted_test=None):
    from sklearn.metrics import classification_report
    print("Train data report:")
    print(classification_report(y_train, predicted_train))
    print("Test data report:")
    print(classification_report(y_test, predicted_test))


def save_test_report_to_tex(y_test, y_predicted, file):
    report = classification_report(y_test, y_predicted, output_dict=True)

    s = """
    \\begin{tabular}{ | c | c | c | c | }
	\hline
	         &presision & recall & count \\\\ \hline
	class1   & %0.2f    & %0.2f  & %0.0f \\\\ \hline
	class2   & %0.2f    & %0.2f  & %0.0f \\\\ \hline
	average  & %0.2f    &        &       \\\\
	\hline
	accuracy & \multicolumn{3}{c|}{%0.2f}\\\\
	\hline
    \end{tabular}""" % (report["1"]["precision"], report["1"]["recall"], report["1"]["support"],
                        report["-1"]["precision"], report["-1"]["recall"], report["-1"]["support"],
                        (report["-1"]["precision"] + report["1"]["precision"]) / 2,
                        report["accuracy"])
    with open(file, "w+") as f:
        f.writelines(s)
    return s
