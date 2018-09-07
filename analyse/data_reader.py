import numpy as np
import scipy.signal as ss
from obci_readmanager.signal_processing.read_manager import ReadManager

from model.config import SAMPLING_RATE as ANALYSIS_SAMPLING_RATE
from utils import ValueWithProps

class Data_Reader(object):

	def __init__(self, filename, T, patient_name, channel_names, reference_channels):
		'''
		:param filename: Name of file that is to be imported
		:param T: Timestamp representing the beginning of the experiment
		:param patient_name: The name of the patient
		:param channel_names: Names of the channels that have EEG signal data
		:param reference_channels: Names of the channels that have reference signals
		:return: Saved file with extracted signals for each patient into an nd Array
		'''
		self.filename = filename
		self.T = T
		self.patient_name = patient_name
		self.channel_names = channel_names
		self.reference_channels = reference_channels

		self.SAMPLING = 2048
		self.NYQUIST_FREQUENCY = self.SAMPLING / 2

		self.read_signals()

		self.filter_signals()

		self.resample_signals()

		self.extract_tags()

		self.extract_classes_from_tags()

		self.fix_classes_to_match_sound()

		self.populate_classes_with_signal()

		self.save_classes_to_file()


	def read_signals(self):

		# The offset of the tMSI amplifier used
		TMSI_OFFSET = 0.0715

		# Initialize the ReadManager
		mgr = ReadManager(self.filename + ".xml", self.filename + ".raw", self.filename + ".tag")

		# Reference Signal Reading
		ear_1 = mgr.get_channels_samples([reference_channels[0]]) * TMSI_OFFSET
		ear_2 = mgr.get_channels_samples([reference_channels[1]]) * TMSI_OFFSET
		ear = (ear_1 + ear_2)/2


		# Reading the data signals for each channel name and mapping them onto a montage array
		signals = []
		for c_name in channel_names:
			signal = mgr.get_channels_samples([c_name])
			signals.append(signal * TMSI_OFFSET - ear)
		self.signals = np.array(signals)


		# Reading the sound channel which has all the sounds
		self.sound = mgr.get_channels_samples(['Aux32'])

	def filter_signals(self):

		# Define used filters
		b_highpass, a_highpass = ss.butter(4, 3 / self.NYQUIST_FREQUENCY, 'highpass')
		b_lowpass, a_lowpass = ss.butter(4, 30 / self.NYQUIST_FREQUENCY, 'low')
		b_notch, a_notch = ss.iirnotch(50 / self.NYQUIST_FREQUENCY, 30)

		# Perform filtering on all signals
		for index, signal in enumerate(self.signals):
			signal = ss.filtfilt(b_notch, a_notch, signal)
			signal = ss.filtfilt(b_highpass, a_highpass, signal)
			signal = ss.filtfilt(b_lowpass, a_lowpass, signal)
			self.signals[index] = signal


	def resample_signals(self):

		# Signal constants for resampling
		NEW_SAMPLING = ANALYSIS_SAMPLING_RATE

		# Designing filter to allow resampling
		b, a = ss.butter(4, NEW_SAMPLING / self.NYQUIST_FREQUENCY, 'low')

		# Filtering and resampling
		signals = []
		for index, signal in enumerate(self.signals):
			signal = ss.filtfilt(b, a, signal)
			signals.append(signal[::self.SAMPLING // NEW_SAMPLING])
		self.signals = np.array(signals)

		sound = ss.filtfilt(b, a, self.sound)
		self.sound = sound[::self.SAMPLING // NEW_SAMPLING]

		# Setting new constants for signal
		self.SAMPLING = NEW_SAMPLING
		self.NYQUIST_FREQUENCY = self.SAMPLING / 2

	def extract_tags(self):

		self.tags = []

		with open(self.patient_name + '/experiment_order.txt') as order:
			with open(self.patient_name + '/tags.txt') as tags_file:
				with open(self.patient_name + '/concentration.txt') as concentration_scores_file:

					order = order.readlines()
					concentration_scores = concentration_scores_file.readlines()
					tag_lines = tags_file.readlines()

					for trial_no, is_high_trial in enumerate(order):
						is_high_trial = bool(is_high_trial.strip())

						for tag in tag_lines[40 * trial_no: 40 * trial_no + 40]:
							tag_array = tag.strip().split(',')

							# Set Tag timestamp to array index
							tag_value = float(tag_array[0])
							tag_value -= self.T
							tag_value *= self.SAMPLING
							tag_value = int(tag_value)

							# Set stimuli type
							tag_type = int(tag_array[1])

							concentration_array = np.array(concentration_scores[trial_no].strip().split(','))
							successful_patient_classifications = concentration_array[0]
							total_correct_stimuli = concentration_array[1]

							trial_type = 'high' if is_high_trial else 'low'
							role = 'train' if successful_patient_classifications == total_correct_stimuli else 'test'

							self.tags.append(
								ValueWithProps(
									tag_value,
									{
										'trail_type': trial_type,
										'role': role,
										'tag_type': tag_type
									}
								)
							)

	def extract_classes_from_tags(self):

		self.classes = []

		for tag in self.tags:
			class_type = 'non_target'

			if tag.props['trail_type'] == 'high' and tag.props['tag_type'] == 1:
				class_type = 'target'

			if tag.props['trail_type'] == 'low' and tag.props['tag_type'] == 0:
				class_type = 'target'

			self.classes.append(
				ValueWithProps(
					tag.value,
					{
						'role': tag.props['role'],
						'class_type': class_type
					}
				)
			)

	def fix_classes_to_match_sound(self):

		self.fixed_classes = []

		for _class in self.classes:
			sound_extract = self.sound[_class.value - self.SAMPLING // 2: _class.value + self.SAMPLING // 2]
			sound_power_threshold = np.max(sound_extract) * 0.5

			for sound_index, sound_value in enumerate(sound_extract):
				if sound_value > sound_power_threshold:
					_class.value += (sound_index - self.SAMPLING // 2)
					break

			self.fixed_classes.append(
				ValueWithProps(
					_class.value,
					_class.props
				)
			)

	def populate_classes_with_signal(self):

		self.populated_classes = []

		for _class in self.fixed_classes:
			low = int(_class.value - 0.1 * self.SAMPLING)
			high = int(_class.value + 0.9 * self.SAMPLING)
			value = self.signals[:, low:high]

			self.populated_classes.append(
				ValueWithProps(
					value,
					_class.props
				)
			)


	def save_classes_to_file(self):

		non_target = ValueWithProps.find(self.populated_classes, {
			'role': 'train',
			'class_type': 'non_target'
		})

		target = ValueWithProps.find(self.populated_classes, {
			'role': 'train',
			'class_type': 'target'
		})

		non_target = np.array(list(map(lambda item: item.value, non_target)))
		target = np.array(list(map(lambda item: item.value, target)))

		X_train = np.vstack((
			non_target[:len(target)],
			target
		))
		y_train = np.hstack((
			np.zeros(target.shape[0]),
			np.ones(target.shape[0])
		))

		np.save('{}_classes'.format(self.patient_name), X_train)
		np.save('{}_labels'.format(self.patient_name), y_train)


if __name__ == '__main__':
	channel_names = ['ExG1', 'ExG2', 'ExG3', 'ExG4', 'ExG5', 'ExG6', 'ExG7', 'ExG8', 'ExG10', 'ExG11', 'ExG12', 'ExG13', 'ExG14', 'ExG16', 'ExG17', 'ExG18', 'ExG19', 'ExG20', 'ExG21', 'ExG22', 'ExG23']
	reference_channels = ['ExG9', 'ExG15']
	Data_Reader('../pawel_auditory', 1.524506533165685E9, '../pawel', channel_names, reference_channels)
	Data_Reader('../lukasz_auditory', 1.524503048304122E9, '../lukasz', channel_names, reference_channels)
	channel_names = ['Fp1', 'Fpz', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T3', 'C3', 'Cz', 'C4', 'T4', 'T5', 'P3', 'Pz', 'P4', 'T6', 'O1', 'Oz', 'O2']
	reference_channels = ['M1', 'M2']
	Data_Reader('../Aniach_auditory', 1.527520873794541E9, '../Ania_Ch', channel_names, reference_channels)
	Data_Reader('../Ania_S_auditory', 1.52752763303048E9, '../Ania_S', channel_names, reference_channels)
	Data_Reader('../Czarek_auditory', 1.527518817046714E9, '../Czarek', channel_names, reference_channels)
	# Data_Reader('../Justyna_auditory', 1.527514410394228E9, '../Justyna', channel_names, reference_channels)
	Data_Reader('../Tomek_auditory', 1.527516716333505E9, '../Tomek', channel_names, reference_channels)
	Data_Reader('../Weronika_auditory', 1.527530160826849E9, '../Weronika', channel_names, reference_channels)

