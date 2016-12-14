from m_c.brick.audio import Audio
from m_c.brick.group import Group
from m_c.brick.power import Power
from m_c.brick.start import Start
from m_c.brick.store import Store


POWER = dict(
    family='01101',
    hostname='datensammel-leitschiene',
    url='http://{hostname}.local',
)
POWER_GROUP = Group(
    'Teardown'
)

POWER_DISK0 = Power(
    'Kleinhirn', POWER_GROUP,
    prime='00010', **POWER
)
POWER_LAMP0 = Power(
    'Light', POWER_GROUP,
    prime='01000', **POWER
)
POWER_TONE0 = Power(
    'Stereo', POWER_GROUP,
    prime='00100', **POWER
)


STORE = dict(prefix='/Volumes', power_delay=30, eject_retry=3, eject_wait=5)

STORE_DISK0 = Store(
    'Kleinhirn', POWER_DISK0,
    **STORE
)
STORE_DISK1 = Store(
    'Großhirn', POWER_GROUP,
    **STORE
)


AUDIO = dict(delay=3)

AUDIO_TONE0 = Audio(
    'Krawallschachtel', POWER_TONE0,
    **AUDIO
)


START = dict()

START_PHOTO = Start(
    'Photos', STORE_DISK0,
    **START
)
START_LIGHT = Start(
    'Lightroom', STORE_DISK0,
    prime='Adobe Photoshop Lightroom 4', **START
)
START_ITUNE = Start(
    'iTunes', STORE_DISK0, AUDIO_TONE0,
    **START
)
START_DEEZE = Start(
    'Deezer', AUDIO_TONE0,
    **START
)
START_MOVIS = Start(
    'Movist', STORE_DISK0, STORE_DISK1, AUDIO_TONE0,
    **START
)
START_BKUP0 = Start(
    'Rsync_K_G', STORE_DISK0, STORE_DISK1,
    prime='/Volumes/Großhirn/disk_fetch.sh', script=True, **START
)
