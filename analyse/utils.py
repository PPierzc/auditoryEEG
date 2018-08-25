import numpy as np
import matplotlib.pyplot as plt

class ValueWithProps (object):
	def __init__(self, value, props):
		self.value = value
		self.props = props

	@staticmethod
	def find(array, query):

		_response_array = []
		keys = dict.keys(query)

		for item in array:
			score = 0

			for key in keys:
				if item.props[key] == query[key]:
					score += 1

			if score == len(keys):
				_response_array.append(item)

		return np.array(_response_array)


def ROC(X, y, model, name=None, path=None):

	indexes = np.arange(0, len(y))
	np.random.shuffle(indexes)

	X = X[indexes]
	y = y[indexes]

	number_of_test_items = int(round(0.7 * len(y)))

	X_train = X[:number_of_test_items]
	y_train = y[:number_of_test_items]
	X_test = X[number_of_test_items:]
	y_test = y[number_of_test_items:]

	model.fit(X_train, y_train, X_test, y_test)

	total = len(y_test)

	plt.figure(figsize=(10, 5))
	plt.suptitle("Patient: {}, Model: {}".format(name, model))

	targets = []
	non_targets = []

	for i in range(total):
		pred = model.predict_proba(X_test[i])
		targets.append(pred) if y_test[i] else non_targets.append(pred)

	plt.subplot(1,2,1)
	plt.hist(non_targets, color=(0, 0.57, 0.69, .2), label="Non-Target")
	plt.hist(targets, color=(1, 0.47, 0, .2), label="Target")
	plt.title("Results Distribution")
	plt.xlabel("Classification Result")
	plt.legend()

	targets = np.array(targets)
	non_targets = np.array(non_targets)

	t_p = []
	f_p = []

	for i in np.arange(-0.01, 1.01, 0.01):
		t_p.append(len(targets[targets > i]) / len(targets))
		f_p.append(len(non_targets[non_targets > i]) / len(non_targets))

	diff_f_p = np.concatenate(([f_p[-1]], np.diff(f_p[::-1])))

	auc = 0
	for i, df in enumerate(diff_f_p):
		auc += t_p[::-1][i] * df
	auc -= t_p[-1] * diff_f_p[-1]/2

	plt.subplot(1, 2, 2)
	plt.plot(f_p, t_p)
	plt.plot([0, 1], [0, 1], ls='--')
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title("AUC: {:.2f}".format(auc))

	if path: plt.savefig(path)

	plt.show()

def bootstrap_error(signals):
	N = 100
	b_sig = []
	for i in range(N):
		indexes = np.random.randint(0, len(signals), 100)
		mean_sig = np.mean(signals[indexes], axis=0)
		b_sig.append(mean_sig)

	b_mean = np.mean(b_sig, axis=0)
	b_std = np.std(b_sig, axis=0)
	return (b_mean, b_std)

signal_data = {
	'X': np.concatenate((
        np.load('../Ania_Ch_classes.npy'),
	    np.load('../Tomek_classes.npy'),
	    np.load('../pawel_classes.npy'),
	    np.load('../lukasz_classes.npy'),
	    np.load('../Czarek_classes.npy'),
	    np.load('../Weronika_classes.npy'),
	    np.load('../Ania_S_classes.npy')
	)),
	'y': np.concatenate((
	    np.load('../Ania_Ch_labels.npy'),
	    np.load('../Tomek_labels.npy'),
	    np.load('../pawel_labels.npy'),
	    np.load('../lukasz_labels.npy'),
	    np.load('../Czarek_labels.npy'),
	    np.load('../Weronika_labels.npy'),
	    np.load('../Ania_S_labels.npy')
	))
}