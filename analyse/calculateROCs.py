from utils import ROC
from utils import getSignalData
import model
import numpy as np

data = getSignalData()

def getGlobalModel(patientKey):
	X_global = []
	y_global = []
	for patient in data['data']['X'].keys():
			if (patient != patientKey):
				X_global.append(data['data']['X'][patient][:, 6:14, :])
				y_global.append(data['data']['y'][patient])
	X_global = np.concatenate(X_global)
	y_global = np.concatenate(y_global)

	models = [m() for m in model.models[:3]]

	indexes = np.arange(0, len(y_global))
	np.random.shuffle(indexes)

	X_global = X_global[indexes]
	y_global = y_global[indexes]

	number_of_test_items = int(round(0.7 * len(y)))

	X_train = X_global[:number_of_test_items]
	y_train = y_global[:number_of_test_items]
	X_test = X_global[number_of_test_items:]
	y_test = y_global[number_of_test_items:]

	return model.models[3](models).fit(X_train, y_train, X_test, y_test)

for patient in data['data']['X'].keys():
	X = data['data']['X'][patient][:, 6:14, :]
	y = data['data']['y'][patient]

	global_model = getGlobalModel(patient)

	for m in model.models[:3]:
		clf = m()
		ROC(X, y, clf, name=patient, path='./rocs/{}_{}.png'.format(clf, patient), show=False)


	models = [m() for m in model.models[:3]]
	clf = model.models[3](models)
	ROC(X, y, clf, name=patient, path='./rocs/{}_{}.png'.format(clf, patient), show=False)

	models = [m() for m in model.models[:3]]
	clf = model.models[4](models, global_model=global_model)
	ROC(X, y, clf, name=patient, path='./rocs/{}_{}'.format(clf, patient), show=False)
