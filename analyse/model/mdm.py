import pyriemann
import numpy as np

from .config import SAMPLING_RATE

class Ensamble_MDM(object):
	def __init__(self):
		self.NUMBER_OF_MODELS = 2
		self.models = []

	def fit(self, X, y, *args, **kwargs):

		X_test = args[0]
		y_test = args[1]

		def test(model, X_test, y_test):
			total = len(y_test)
			correct = 0

			for i in range(total):
				cov = pyriemann.estimation.Covariances().fit_transform(X_test[i].reshape(1, 8, SAMPLING_RATE))
				if model.predict(cov) == y_test[i]:
					correct += 1

			acc = correct / total

			return acc

		for i in range(self.NUMBER_OF_MODELS):
			print(i)
			bootstrap_indexes = np.random.randint(0, X.shape[0], X.shape[0])

			X_bootstrap = X[bootstrap_indexes]
			y_bootstrap = y[bootstrap_indexes]

			cov = pyriemann.estimation.Covariances().fit_transform(X_bootstrap)

			mdm = pyriemann.classification.MDM()

			mdm.fit(cov, y_bootstrap)

			t_neg = test(mdm, X_test, y_test)

			self.models.append({
				'model': mdm,
				'true_negative': t_neg
			})

	def predict(self, X):
		cov = pyriemann.estimation.Covariances().fit_transform(X.reshape(1, 8, SAMPLING_RATE))

		prediction = np.zeros(2)

		for model in self.models:
			if model['model'].predict(cov):
				prediction[1] += model['true_negative']
			else:
				prediction[0] += model['true_negative']

		prediction = np.where(prediction == max(prediction))[0][0]

		return prediction

	def predict_proba(self, X):
		cov = pyriemann.estimation.Covariances().fit_transform(X.reshape(1, 8, SAMPLING_RATE))

		prediction = np.zeros(2)
		total_possible = 0

		for model in self.models:
			total_possible += model['true_negative']
			if model['model'].predict(cov):
				prediction[1] += model['true_negative']
			else:
				prediction[0] += model['true_negative']

		return prediction[1] / total_possible

	def __str__(self):
		return 'Ensamble_MDM'
