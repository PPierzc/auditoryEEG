from utils import ROC
from utils import getSignalData
import model

data = getSignalData()
X = data['X'][:, 6:14, :]
y = data['y']


for m in model.models:
	print(m())
	ROC(X, y, m(), name=None, path=None)