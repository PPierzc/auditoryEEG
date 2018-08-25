import numpy as np
import matplotlib.pyplot as plt

from .utils import bootstrap_error, signal_data

def ERP(X, y, channel_id):
	X_target = X[y == 1]
	X_non_target = X[y == 0]

	ERP_target, STD_target = bootstrap_error(X_target)
	ERP_non_target, STD_non_target = bootstrap_error(X_non_target)

	np.save('../erp.npy', ERP_target[channel_id])
	np.save('../non_erp.npy', ERP_non_target[channel_id])

	plt.figure(figsize=(10,7))

	plt.subplot(2,1,1)
	plt.suptitle('Templates for LDA classification')
	plt.plot(np.arange(-0.1, 0.9, 1/2048), ERP_target[channel_id], c='#FF7800', label='target')
	plt.fill_between(np.arange(-0.1, 0.9, 1/2048), ERP_target[channel_id] - STD_target[channel_id], ERP_target[channel_id] + STD_target[channel_id], color=(1,0.47,0, .2))
	plt.ylabel('$\mu$V')

	plt.subplot(2,1,2)
	plt.plot(np.arange(-0.1, 0.9, 1/2048), ERP_non_target[channel_id], c='#0091B2', label='non-target')
	plt.fill_between(np.arange(-0.1, 0.9, 1/2048), ERP_non_target[channel_id] - STD_non_target[channel_id], ERP_non_target[channel_id] + STD_non_target[channel_id], color=(0,0.57,0.69, .2))
	plt.xlabel('Time since event [s]')
	plt.ylabel('$\mu$V')

	plt.savefig('auditory_erp.png')
	plt.show()

if __name__ == '__main__':
	X = signal_data['X']
	y = signal_data['y']

	channel_id = 9

	ERP(X, y, channel_id)

