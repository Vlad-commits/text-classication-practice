import itertools

from statistics import median
import cplex
import numpy as np
from sklearn.base import BaseEstimator


def from_sparse(sparse_matrix, columns_size):
    m = []
    for row_sparse in sparse_matrix:
        row = []
        k = 0
        for i in range(columns_size):
            if i in row_sparse[0]:
                row.append(row_sparse[1][k])
                k = k + 1
            else:
                row.append(0)
        m.append(row)
    for i in range(columns_size):
        for j in range(columns_size):
            print(m[i][j])
            print(m[j][i])
            assert m[i][j] == m[j][i]


def to_sparse(matrix):
    sparse_matrix = []
    for row in matrix:
        non_zero_row_indexes = []
        non_zero_row_values = []
        for i in range(len(row)):
            if row[i] != 0:
                non_zero_row_indexes.append(i)
                non_zero_row_values.append(row[i])
        sparse_matrix.append([non_zero_row_indexes, non_zero_row_values])
    return sparse_matrix


def scalar_multiply(list_vector, list_vector2):
    assert len(list_vector) == len(list_vector2)
    result = 0
    for i in range(len(list_vector)):
        result = result + list_vector[i] * list_vector2[i]
    return result


def create_qp_solver(c: int, y_list, x_matrix):
    p = cplex.Cplex()
    size = len(y_list)
    assert size == len(x_matrix)
    p.objective.set_sense(p.objective.sense.minimize)

    linear = list(itertools.repeat(-1, size))
    lb = list(itertools.repeat(0, size))
    ub = list(itertools.repeat(c, size))

    p.variables.add(obj=linear, lb=lb, ub=ub)

    p.linear_constraints.add(rhs=[0],
                             lin_expr=[[list(range(size)), [i * 1.0 for i in list(y_list)]]],
                             senses="E")

    qmat = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(i, size):
            qmat[i][j] = y_list[i] * y_list[j] * scalar_multiply(x_matrix[i], x_matrix[j]) * 0.5
            if i != j:
                qmat[i][j] = qmat[i][j] / 2
            qmat[j][i] = qmat[i][j]

    qmat_sparse = to_sparse(qmat)

    p.objective.set_quadratic(qmat_sparse)
    return p


class Model(BaseEstimator):
    _estimator_type = "classifier"
    w = {}
    b = {}
    c = 1
    eps = 0.000001
    use_svd = False
    transformation_matrix = None

    x_mean = {}

    def __init__(self, c, use_svd=False):
        assert c != 0
        self.c = c
        self.use_svd = use_svd

    def transform_features(self, x):
        x = x - self.x_mean
        if self.use_svd:
            return np.matmul(x, self.transformation_matrix)
        else:
            return x

    def reverse_transform(self, x):
        if self.use_svd:
            x = np.matmul(x, self.transformation_matrix)
        return x + self.x_mean

    def fit(self, x, y, verbose=False):
        self.x_mean = x.mean(axis=0)
        if self.use_svd:
            u, s, vh = np.linalg.svd(x.transpose(), full_matrices=True)
            self.transformation_matrix = u[:, 0:2]
            if verbose:
                print("Transformation_matrix is:")
                print(self.transformation_matrix)

        x = self.transform_features(x)

        p = create_qp_solver(self.c, y, x)

        if not verbose:
            p.set_log_stream(None)
            p.set_results_stream(None)

        p.solve()

        if verbose:
            print("Solution status = ", p.solution.get_status(), ":", end=' ')
            print(p.solution.status[p.solution.get_status()])
            print("Solution value  = ", p.solution.get_objective_value())
            numrows = p.linear_constraints.get_num()
            for i in range(numrows):
                print("Row ", i, ":  ", end=' ')
                print("Slack = %10f " % p.solution.get_linear_slacks(i), end=' ')
                print("Pi = %10f" % p.solution.get_dual_values(i))

            numcols = p.variables.get_num()
            for j in range(numcols):
                print("Column ", j, ":  ", end=' ')
                print("Value = %10f " % p.solution.get_values(j), end=' ')
                print("Reduced Cost = %10f" % p.solution.get_reduced_costs(j))

        size = len(y)
        self.w = list(itertools.repeat(0, len(x[0])))
        for i in range(size):
            for j in range(len(x[0])):
                self.w[j] = self.w[j] + p.solution.get_values(i) * y[i] * x[i][j]

        bs = []
        for j in range(p.variables.get_num()):
            lambda_j = p.solution.get_values(j)
            if (abs(lambda_j) > self.eps) & (abs(lambda_j) < self.c - self.eps):
                # if (abs(lambda_j) > self.eps) :

                b = scalar_multiply(self.w, x[j]) - y[j]
                bs.append(b)

        self.b = median(bs)

        return self.w, self.b

    def predict_one(self, x):
        x_transformed = self.transform_features(x)
        return 1 if scalar_multiply(x_transformed, self.w) - self.b > 0 else -1

    def predict(self, xs):
        return [self.predict_one(x) for x in xs]

    def get_params(self, deep=True):
        return {"c": self.c,
                "use_svd": self.use_svd}
