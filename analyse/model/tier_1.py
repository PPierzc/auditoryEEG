import numpy as np

class Tier_1_Model(object):
    def __init__(self, models):
        self.models = models

    def fit(self, X, y, X_test, y_test):

        for model_index in range(len(self.models)):
            total = len(y_test)
            correct = 0
            f_p = 0

            self.models[model_index].fit(X, y, X_test, y_test)

            for i in range(total):
                if self.models[model_index].predict(X_test[i]) == y_test[i]:
                    correct += 1
                elif self.models[model_index].predict(X_test[i]) == 1:
                    f_p += 1

    def predict(self, X):
        prediction = np.zeros(2)

        for index, model in enumerate(self.models):
            if model.predict(X):
                prediction[1] += 1
            else:
                prediction[0] += 1

        return np.where(prediction == max(prediction))[0][0]

    def predict_proba(self, X):
        prediction = 0

        for model in self.models:
            prediction += model.predict_proba(X)

        return prediction / len(self.models)

    def __str__(self):
        return 'Tier 1 Model'
