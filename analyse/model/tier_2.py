import numpy as np

from .tier_1 import Tier_1_Model

class Tier_2_Model(object):

    def __init__(self, *args, **kwargs):
        if kwargs['global_model']:
            self.global_model = kwargs['global_model']
        else:
            self.global_model = None

        self.models = args

    def fit(self, *args):
        if not self.global_model:
            self.global_model = Tier_1_Model(self.models)

            indexes = np.arange(0, len(args[1]))
            np.random.shuffle(indexes)

            X = args[0][indexes]
            y = args[1][indexes]

            no_test = int(round(0.8 * len(y)))

            X_train = X[:no_test]
            y_train = y[:no_test]
            X_test = X[no_test:]
            y_test = y[no_test:]

            self.global_model.fit(X_train, y_train, X_test, y_test)

        self.specific_model = Tier_1_Model(self.models)

        if not self.global_model:
            indexes = np.arange(0, len(args[3]))
            np.random.shuffle(indexes)

            X = args[2][indexes]
            y = args[3][indexes]

        else:
            indexes = np.arange(0, len(args[1]))
            np.random.shuffle(indexes)

            X = args[0][indexes]
            y = args[1][indexes]

        no_test = int(round(0.8 * len(y)))

        X_train = X[:no_test]
        y_train = y[:no_test]
        X_test = X[no_test:]
        y_test = y[no_test:]

        self.specific_model.fit(X_train, y_train, X_test, y_test)

    def predict(self, X):
        prediction = np.zeros(2)

        for index, model in enumerate([self.specific_model, self.global_model]):
            if model.predict(X):
                prediction[1] += 1
            else:
                prediction[0] += 1

        return np.where(prediction == max(prediction))[0][0]

    def predict_proba(self, X):
        prediction = 0

        for model in [self.specific_model, self.global_model]:
            prediction += model.predict_proba(X)

        return prediction/2

    def __str__(self):
        return 'Tier 2 Model'
