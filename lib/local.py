from lib.brick.audio import Audio
from lib.brick.group import Group
from lib.brick.power import Power
from lib.brick.start import Start
from lib.brick.store import Store

GROUP_TEARD = Group(
    'Teardown'
)

POWER = dict(
    family='01101',
    hostname='datensammel-leitschiene',
    url='http://{hostname}.local',
)
POWER_DISK0 = Power(
    'Kleinhirn', GROUP_TEARD, prime='00010', **POWER
)
POWER_LAMP0 = Power(
    'Light', GROUP_TEARD, prime='01000', **POWER
)
POWER_TONE0 = Power(
    'Stereo', GROUP_TEARD, prime='00100', **POWER
)


STORE = dict(eject_retry=3, eject_wait=5, power_delay=30)
STORE_DISK0 = Store(
    'Kleinhirn', POWER_DISK0, **STORE
)
STORE_DISK1 = Store(
    'Großhirn', GROUP_TEARD, **STORE
)


AUDIO_TONE0 = Audio(
    'Krawallschachtel', POWER_TONE0, delay=3
)


START_PHOTO = Start(
    'Photos', STORE_DISK0
)
START_LIGHT = Start(
    'Lightroom', STORE_DISK0, prime='Adobe Photoshop Lightroom 4'
)
START_ITUNE = Start(
    'iTunes', STORE_DISK0, AUDIO_TONE0
)
START_DEEZE = Start(
    'Deezer', AUDIO_TONE0
)
START_MOVIS = Start(
    'Movist', STORE_DISK0, STORE_DISK1, AUDIO_TONE0
)
START_BKUP0 = Start(
    'Rsync_K_G', STORE_DISK0, STORE_DISK1,
    prime='/Volumes/Großhirn/disk_fetch.sh', script=True
)
