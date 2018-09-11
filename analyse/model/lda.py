import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

from .config import SAMPLING_RATE

class Ensamble_LDA(object):
    def __init__(self):
        self.model = LDA()

        self.ERP = np.load('../erp.npy')
        self.ERP /= np.linalg.norm(self.ERP)

        self.non_ERP = np.load('../non_erp.npy')
        self.non_ERP /= np.linalg.norm(self.non_ERP)

    def fit(self, X, y, *args, **kwargs):

        features = []

        for i in range(8):
            features.append(np.dot(X[:, i, :], self.ERP))
            features.append(np.dot(X[:, i, :], self.non_ERP))

        X = np.dstack(features)[0]

        self.model.fit(X, y)

    def predict(self, X):

        X = X.reshape(1, 8, SAMPLING_RATE)

        features = []

        for i in range(8):
            features.append(np.dot(X[:, i, :], self.ERP))
            features.append(np.dot(X[:, i, :], self.non_ERP))

        X = np.dstack(features)[0]

        return 1 if self.model.predict_proba(X)[0][1] > 0.7 else 0

    def predict_proba(self, X):

        X = X.reshape(1, 8, SAMPLING_RATE)

        features = []

        for i in range(8):
            features.append(np.dot(X[:, i, :], self.ERP))
            features.append(np.dot(X[:, i, :], self.non_ERP))

        X = np.dstack(features)[0]

        return self.model.predict_proba(X)[0][1]

    def __str__(self):
        return 'Ensamble_LDA'

    def __repr__(self):
        return 'Ensamble_LDA'
