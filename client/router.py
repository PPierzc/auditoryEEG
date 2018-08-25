from views.menu import Menu
from views.record_setup import RecordSetup
from views.record_trials import RecordTrials

router = {
	'menu': Menu,
	'record_setup': RecordSetup,
	'record_trials': RecordTrials
}