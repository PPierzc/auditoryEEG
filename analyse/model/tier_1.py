import numpy as np

class Tier_1_Model(object):
    def __init__(self, models):
        self.models = models

    def fit(self, X, y, *args):

        for model_index in range(len(self.models)):
            self.models[model_index].fit(X, y, *args)

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

    def __repr__(self):
        return 'Tier 1 Model'
